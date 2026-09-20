import SwiftUI

struct SystemStatusScreen: View {
  let model: SystemStatusViewModel

  var body: some View {
    VStack(spacing: AppSpacing.md) {
      Text("System status").font(.title2).foregroundStyle(AppColors.onSurface)
      status
      AppButton(label: "Refresh") { Task { await model.refresh() } }
    }
    .padding(AppSpacing.lg)
    .frame(maxWidth: .infinity, maxHeight: .infinity)
    .background(AppColors.background)
    .task { await model.refresh() }
  }

  @ViewBuilder private var status: some View {
    switch model.state {
    case .loading:
      ProgressView().accessibilityLabel("Loading system status")
    case .content(let databaseReady):
      Text(databaseReady ? "Database ready" : "Database not ready")
        .accessibilityIdentifier("database-status")
        .foregroundStyle(AppColors.onSurface)
    case .failure:
      Text("Unable to load system status.")
        .accessibilityIdentifier("system-error")
        .foregroundStyle(AppColors.onSurface)
    }
  }
}
