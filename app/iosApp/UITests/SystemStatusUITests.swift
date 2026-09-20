import XCTest

final class SystemStatusUITests: XCTestCase {
  @MainActor
  func testRendersStatusAndRefresh() {
    let app = XCUIApplication()
    app.launch()
    XCTAssertTrue(app.staticTexts["System status"].waitForExistence(timeout: 10))
    let refresh = app.buttons["Refresh"]
    XCTAssertTrue(refresh.exists)
    let status = app.staticTexts["database-status"]
    let error = app.staticTexts["system-error"]
    XCTAssertTrue(status.waitForExistence(timeout: 15) || error.exists)
    refresh.tap()
    XCTAssertTrue(status.waitForExistence(timeout: 15) || error.exists)
  }
}
