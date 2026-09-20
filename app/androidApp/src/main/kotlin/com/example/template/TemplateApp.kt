package com.example.template

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import com.example.template.core.designsystem.TemplateTheme
import com.example.template.feature.system.SystemStatusScreen
import com.example.template.feature.system.SystemStatusViewModel
import com.example.template.shared.feature.system.data.ApolloSystemStatusRepository
import com.example.template.shared.feature.system.domain.GetSystemStatusUseCase

@Composable
fun TemplateApp() {
    val viewModel: SystemStatusViewModel =
        viewModel(
            factory =
                viewModelFactory {
                    initializer {
                        SystemStatusViewModel(
                            GetSystemStatusUseCase(
                                ApolloSystemStatusRepository(BuildConfig.GRAPHQL_URL)
                            )
                        )
                    }
                }
        )
    val state by viewModel.state.collectAsStateWithLifecycle()
    LaunchedEffect(Unit) { viewModel.refresh() }
    TemplateTheme { SystemStatusScreen(state, viewModel::refresh) }
}
