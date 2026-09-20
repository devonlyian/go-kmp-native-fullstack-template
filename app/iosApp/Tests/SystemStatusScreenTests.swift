import Testing

@testable import TemplateApp

@MainActor
struct SystemStatusScreenTests {
  @Test func loadsReadinessAndRefreshes() async {
    var calls = 0
    let model = SystemStatusViewModel {
      calls += 1
      return calls == 1
    }
    #expect(model.state == .loading)
    await model.refresh()
    #expect(model.state == .content(databaseReady: true))
    await model.refresh()
    #expect(model.state == .content(databaseReady: false))
  }

  @Test func handlesFailureAndCanRetry() async {
    struct Offline: Error {}
    var calls = 0
    let model = SystemStatusViewModel {
      calls += 1
      if calls == 1 { throw Offline() }
      return true
    }
    await model.refresh()
    #expect(model.state == .failure)
    await model.refresh()
    #expect(model.state == .content(databaseReady: true))
  }
}
