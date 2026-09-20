import SwiftUI

struct AppButton: View {
  let label: LocalizedStringKey
  let action: () -> Void

  var body: some View {
    Button(label, action: action)
      .buttonStyle(.borderedProminent)
      .tint(AppColors.primary)
      .frame(maxWidth: .infinity)
  }
}
