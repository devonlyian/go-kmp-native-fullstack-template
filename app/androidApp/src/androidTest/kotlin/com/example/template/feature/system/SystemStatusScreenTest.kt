package com.example.template.feature.system

import androidx.activity.ComponentActivity
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.v2.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import org.junit.Assert.assertEquals
import org.junit.Rule
import org.junit.Test

class SystemStatusScreenTest {
    @get:Rule val composeRule = createAndroidComposeRule<ComponentActivity>()

    @Test
    fun displaysReadyStatus() {
        var refreshes = 0
        composeRule.setContent {
            SystemStatusScreen(SystemStatusScreenState.Content(true), { refreshes++ })
        }
        composeRule.onNodeWithText("Database ready").assertIsDisplayed()
        composeRule.onNodeWithTag("refresh-button").assertIsDisplayed().performClick()
        composeRule.runOnIdle { assertEquals(1, refreshes) }
    }

    @Test
    fun displaysFailureStatus() {
        composeRule.setContent {
            SystemStatusScreen(SystemStatusScreenState.Error("Unable to load system status."), {})
        }
        composeRule.onNodeWithTag("system-error").assertIsDisplayed()
    }
}
