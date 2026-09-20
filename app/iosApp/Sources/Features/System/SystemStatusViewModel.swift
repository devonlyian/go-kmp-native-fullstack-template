import Foundation
import Observation
import Shared

@MainActor
@Observable
final class SystemStatusViewModel {
  enum State: Equatable {
    case loading
    case content(databaseReady: Bool)
    case failure
  }

  private(set) var state: State = .loading
  private let load: () async throws -> Bool
  private let useCase: GetSystemStatusUseCase?
  private var isRefreshing = false

  init(load: (() async throws -> Bool)? = nil) {
    if let load {
      self.load = load
      useCase = nil
    } else {
      #if DEBUG
        let endpoint = "http://localhost:8080/graphql"
      #else
        let endpoint = "https://api.example.com/graphql"
      #endif
      let useCase = GetSystemStatusUseCase(
        repository: ApolloSystemStatusRepository(endpoint: endpoint)
      )
      self.useCase = useCase
      self.load = { try await useCase.fetch().databaseReady }
    }
  }

  isolated deinit { useCase?.close() }

  func refresh() async {
    guard !isRefreshing else { return }
    isRefreshing = true
    defer { isRefreshing = false }
    state = .loading
    do {
      let ready = try await load()
      try Task.checkCancellation()
      state = .content(databaseReady: ready)
    } catch is CancellationError {
      return
    } catch {
      state = .failure
    }
  }
}
