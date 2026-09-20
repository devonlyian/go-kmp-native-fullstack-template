package graphql

import (
	"bytes"
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"testing"

	"example.com/template/backend/internal/system/application"
	"example.com/template/backend/internal/system/repository"
	"github.com/jackc/pgx/v5/pgxpool"
)

func testRouter() http.Handler {
	system := application.New(repository.New(nil))
	return NewRouter(&Resolver{System: system})
}

func TestHealthEndpoints(t *testing.T) {
	handler := testRouter()
	for _, path := range []string{"/livez", "/readyz"} {
		recorder := httptest.NewRecorder()
		handler.ServeHTTP(recorder, httptest.NewRequest(http.MethodGet, path, nil))
		want := http.StatusNoContent
		if path == "/readyz" {
			want = http.StatusServiceUnavailable
		}
		if recorder.Code != want {
			t.Fatalf("%s status = %d, want %d", path, recorder.Code, want)
		}
	}
}

func TestSystemStatusReturnsFalseWithoutDatabase(t *testing.T) {
	recorder := httptest.NewRecorder()
	request := httptest.NewRequest(http.MethodPost, "/graphql", strings.NewReader(`{"query":"{ systemStatus { databaseReady } }"}`))
	request.Header.Set("Content-Type", "application/json")
	testRouter().ServeHTTP(recorder, request)
	if recorder.Code != http.StatusOK || !strings.Contains(recorder.Body.String(), `"databaseReady":false`) {
		t.Fatalf("unexpected GraphQL response: status=%d body=%s", recorder.Code, recorder.Body.String())
	}
}

func TestGraphQLErrorsAreSanitized(t *testing.T) {
	recorder := httptest.NewRecorder()
	request := httptest.NewRequest(http.MethodPost, "/graphql", strings.NewReader(`{"query":"{ missingField }"}`))
	request.Header.Set("Content-Type", "application/json")
	testRouter().ServeHTTP(recorder, request)
	if !strings.Contains(recorder.Body.String(), "request failed") {
		t.Fatalf("GraphQL error was not sanitized: %s", recorder.Body.String())
	}
}

func TestGraphQLRejectsLargeBodies(t *testing.T) {
	recorder := httptest.NewRecorder()
	body := []byte(`{"query":"` + strings.Repeat("x", maxRequestBody) + `"}`)
	request := httptest.NewRequest(http.MethodPost, "/graphql", bytes.NewReader(body))
	request.Header.Set("Content-Type", "application/json")
	testRouter().ServeHTTP(recorder, request)
	if recorder.Code != http.StatusRequestEntityTooLarge {
		t.Fatalf("large request status = %d, want %d", recorder.Code, http.StatusRequestEntityTooLarge)
	}
	if strings.Contains(recorder.Body.String(), "database") {
		t.Fatalf("large request exposed internal detail: %s", recorder.Body.String())
	}
}

func TestSystemStatusReturnsFalseWhenDatabaseIsUnavailable(t *testing.T) {
	pool, err := pgxpool.New(t.Context(), "postgres://template:template@127.0.0.1:1/template?connect_timeout=1")
	if err != nil {
		t.Fatal("create unavailable database pool")
	}
	t.Cleanup(pool.Close)
	system := application.New(repository.New(pool))
	recorder := httptest.NewRecorder()
	request := httptest.NewRequest(http.MethodPost, "/graphql", strings.NewReader(`{"query":"{ systemStatus { databaseReady } }"}`))
	request.Header.Set("Content-Type", "application/json")
	NewRouter(&Resolver{System: system}).ServeHTTP(recorder, request)
	if recorder.Code != http.StatusOK || !strings.Contains(recorder.Body.String(), `"databaseReady":false`) {
		t.Fatalf("unexpected unavailable database response: status=%d body=%s", recorder.Code, recorder.Body.String())
	}
}

func TestGraphQLComplexityErrorsAreSanitized(t *testing.T) {
	fields := make([]string, 101)
	for i := range fields {
		fields[i] = fmt.Sprintf("f%d: systemStatus { databaseReady }", i)
	}
	recorder := httptest.NewRecorder()
	request := httptest.NewRequest(http.MethodPost, "/graphql", strings.NewReader(`{"query":"{ `+strings.Join(fields, " ")+` }"}`))
	request.Header.Set("Content-Type", "application/json")
	testRouter().ServeHTTP(recorder, request)
	if !strings.Contains(recorder.Body.String(), "request failed") {
		t.Fatalf("complexity error was not sanitized: %s", recorder.Body.String())
	}
}

func TestSystemStatusGraphQLIntegration(t *testing.T) {
	url := os.Getenv("TEST_DATABASE_URL")
	if url == "" {
		t.Skip("TEST_DATABASE_URL is not set")
	}
	pool, err := pgxpool.New(t.Context(), url)
	if err != nil {
		t.Fatal("create test database pool")
	}
	t.Cleanup(pool.Close)
	system := application.New(repository.New(pool))
	recorder := httptest.NewRecorder()
	request := httptest.NewRequest(http.MethodPost, "/graphql", strings.NewReader(`{"query":"{ systemStatus { databaseReady } }"}`))
	request.Header.Set("Content-Type", "application/json")
	NewRouter(&Resolver{System: system}).ServeHTTP(recorder, request)
	if recorder.Code != http.StatusOK || !strings.Contains(recorder.Body.String(), `"databaseReady":true`) {
		t.Fatalf("unexpected GraphQL integration response: status=%d body=%s", recorder.Code, recorder.Body.String())
	}
	pool.Close()
	recorder = httptest.NewRecorder()
	request = httptest.NewRequest(http.MethodPost, "/graphql", strings.NewReader(`{"query":"{ systemStatus { databaseReady } }"}`))
	request.Header.Set("Content-Type", "application/json")
	NewRouter(&Resolver{System: system}).ServeHTTP(recorder, request)
	if recorder.Code != http.StatusOK || !strings.Contains(recorder.Body.String(), `"databaseReady":false`) {
		t.Fatalf("unexpected closed-pool response: status=%d body=%s", recorder.Code, recorder.Body.String())
	}
}
