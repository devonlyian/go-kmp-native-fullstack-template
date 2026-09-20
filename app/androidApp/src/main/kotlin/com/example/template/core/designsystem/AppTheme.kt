package com.example.template.core.designsystem

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.unit.dp

object AppColors {
    val background
        @Composable get() = MaterialTheme.colorScheme.background

    val onSurface
        @Composable get() = MaterialTheme.colorScheme.onSurface

    val primary
        @Composable get() = MaterialTheme.colorScheme.primary
}

object AppSpacing {
    val md = 16.dp
    val lg = 24.dp
}

@Composable
fun TemplateTheme(content: @Composable () -> Unit) =
    MaterialTheme(
        colorScheme = if (isSystemInDarkTheme()) darkColorScheme() else lightColorScheme(),
        content = content,
    )
