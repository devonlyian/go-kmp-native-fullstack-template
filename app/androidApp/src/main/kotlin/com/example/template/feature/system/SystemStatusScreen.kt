package com.example.template.feature.system

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.testTag
import com.example.template.core.designsystem.AppButton
import com.example.template.core.designsystem.AppColors
import com.example.template.core.designsystem.AppSpacing

@Composable
fun SystemStatusScreen(state: SystemStatusScreenState, onRefresh: () -> Unit) {
    Surface(color = AppColors.background, contentColor = AppColors.onSurface) {
        Column(
            modifier = Modifier.fillMaxSize().safeDrawingPadding().padding(AppSpacing.lg),
            verticalArrangement = Arrangement.spacedBy(AppSpacing.md, Alignment.CenterVertically),
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            Text(
                "System status",
                style = MaterialTheme.typography.titleLarge,
                color = AppColors.onSurface,
            )
            when (state) {
                SystemStatusScreenState.Loading ->
                    CircularProgressIndicator(
                        Modifier.semantics {
                            testTag = "system-loading"
                            contentDescription = "Loading system status"
                        }
                    )
                is SystemStatusScreenState.Content ->
                    Text(
                        text = if (state.databaseReady) "Database ready" else "Database not ready",
                        modifier = Modifier.semantics { testTag = "database-status" },
                    )
                is SystemStatusScreenState.Error ->
                    Text(state.message, modifier = Modifier.semantics { testTag = "system-error" })
            }
            AppButton(
                "Refresh",
                onRefresh,
                Modifier.fillMaxWidth().semantics { testTag = "refresh-button" },
            )
        }
    }
}
