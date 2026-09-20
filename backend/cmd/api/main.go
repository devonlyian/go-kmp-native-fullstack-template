package main

import (
	"context"
	"errors"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	systemgraphql "example.com/template/backend/internal/graphql"
	"example.com/template/backend/internal/system/application"
	"example.com/template/backend/internal/system/repository"
	"github.com/jackc/pgx/v5/pgxpool"
)

const shutdownTimeout = 10 * time.Second

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
	pool, err := newPool(context.Background(), os.Getenv("DATABASE_URL"))
	if err != nil {
		logger.Error("database pool configuration failed")
		os.Exit(1)
	}
	if pool != nil {
		defer pool.Close()
	}

	system := application.New(repository.New(pool))
	server := &http.Server{
		Addr:              httpAddress(),
		Handler:           systemgraphql.NewRouter(&systemgraphql.Resolver{System: system}),
		ReadHeaderTimeout: 5 * time.Second,
		ReadTimeout:       10 * time.Second,
		WriteTimeout:      15 * time.Second,
		IdleTimeout:       60 * time.Second,
	}

	go func() {
		logger.Info("http server started", "address", server.Addr)
		if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
			logger.Error("http server failed")
			os.Exit(1)
		}
	}()

	stop := make(chan os.Signal, 1)
	signal.Notify(stop, os.Interrupt, syscall.SIGTERM)
	<-stop
	ctx, cancel := context.WithTimeout(context.Background(), shutdownTimeout)
	defer cancel()
	if err := server.Shutdown(ctx); err != nil {
		logger.Error("http server shutdown failed")
	}
}

func httpAddress() string {
	if address := os.Getenv("HTTP_ADDR"); address != "" {
		return address
	}
	return "127.0.0.1:8080"
}

func newPool(ctx context.Context, databaseURL string) (*pgxpool.Pool, error) {
	if databaseURL == "" {
		return nil, nil
	}
	config, err := pgxpool.ParseConfig(databaseURL)
	if err != nil {
		return nil, err
	}
	return pgxpool.NewWithConfig(ctx, config)
}
