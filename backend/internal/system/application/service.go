package application

import (
	"context"

	"example.com/template/backend/internal/system/domain"
	"example.com/template/backend/internal/system/repository"
)

type Service struct {
	repository *repository.Repository
}

func New(repository *repository.Repository) *Service {
	return &Service{repository: repository}
}

func (s *Service) Status(ctx context.Context) domain.Status {
	if s == nil || s.repository == nil {
		return domain.Status{}
	}
	return domain.Status{DatabaseReady: s.repository.DatabaseReady(ctx)}
}
