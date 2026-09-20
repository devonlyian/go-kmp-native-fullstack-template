package graphql

import (
	"context"
	"net/http"

	"example.com/template/backend/internal/graphql/generated"
	"github.com/99designs/gqlgen/graphql/handler"
	"github.com/99designs/gqlgen/graphql/handler/extension"
	"github.com/vektah/gqlparser/v2/gqlerror"
)

const maxRequestBody = 1 << 20

func NewHTTPHandler(resolver *Resolver) http.Handler {
	server := handler.NewDefaultServer(generated.NewExecutableSchema(generated.Config{Resolvers: resolver}))
	server.Use(extension.FixedComplexityLimit(100))
	server.SetErrorPresenter(func(context.Context, error) *gqlerror.Error {
		return gqlerror.Errorf("request failed")
	})
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.ContentLength > maxRequestBody {
			http.Error(w, "request too large", http.StatusRequestEntityTooLarge)
			return
		}
		http.MaxBytesHandler(server, maxRequestBody).ServeHTTP(w, r)
	})
}

func NewRouter(resolver *Resolver) http.Handler {
	mux := http.NewServeMux()
	mux.Handle("/graphql", NewHTTPHandler(resolver))
	mux.HandleFunc("GET /livez", func(w http.ResponseWriter, _ *http.Request) {
		w.WriteHeader(http.StatusNoContent)
	})
	mux.HandleFunc("GET /readyz", func(w http.ResponseWriter, r *http.Request) {
		if resolver != nil && resolver.System != nil && resolver.System.Status(r.Context()).DatabaseReady {
			w.WriteHeader(http.StatusNoContent)
			return
		}
		w.WriteHeader(http.StatusServiceUnavailable)
	})
	return mux
}
