package repository

import (
	"context"
	"time"

	"example.com/template/backend/db/generated"
	"github.com/jackc/pgx/v5/pgxpool"
)

const checkTimeout = 2 * time.Second

type Repository struct {
	pool    *pgxpool.Pool
	queries *generated.Queries
}

func New(pool *pgxpool.Pool) *Repository {
	if pool == nil {
		return &Repository{}
	}
	return &Repository{pool: pool, queries: generated.New(pool)}
}

func (r *Repository) DatabaseReady(ctx context.Context) bool {
	if r.queries == nil {
		return false
	}
	ctx, cancel := context.WithTimeout(ctx, checkTimeout)
	defer cancel()
	_, err := r.queries.DatabaseReady(ctx)
	return err == nil
}
