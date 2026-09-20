import SwiftUI

@main
struct TemplateApp: App {
  @State private var model = SystemStatusViewModel()

  var body: some Scene {
    WindowGroup { SystemStatusScreen(model: model) }
  }
}
