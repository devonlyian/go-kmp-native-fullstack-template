package repository

import (
	"context"
	"os"
	"testing"

	"github.com/jackc/pgx/v5/pgxpool"
)

func TestDatabaseReadyIntegration(t *testing.T) {
	url := os.Getenv("TEST_DATABASE_URL")
	if url == "" {
		t.Skip("TEST_DATABASE_URL is not set")
	}
	pool, err := pgxpool.New(context.Background(), url)
	if err != nil {
		t.Fatal("create test database pool")
	}
	t.Cleanup(pool.Close)
	if !New(pool).DatabaseReady(context.Background()) {
		t.Fatal("DatabaseReady returned false")
	}
}
