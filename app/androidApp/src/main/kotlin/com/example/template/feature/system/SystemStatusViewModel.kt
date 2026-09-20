package com.example.template.feature.system

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.template.shared.feature.system.domain.GetSystemStatusUseCase
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

sealed interface SystemStatusScreenState {
    data object Loading : SystemStatusScreenState

    data class Content(val databaseReady: Boolean) : SystemStatusScreenState

    data class Error(val message: String) : SystemStatusScreenState
}

class SystemStatusViewModel(private val getSystemStatus: GetSystemStatusUseCase) : ViewModel() {
    private val mutableState =
        MutableStateFlow<SystemStatusScreenState>(SystemStatusScreenState.Loading)
    val state: StateFlow<SystemStatusScreenState> = mutableState.asStateFlow()

    private var refreshJob: Job? = null

    fun refresh() {
        if (refreshJob?.isActive == true) return
        refreshJob = viewModelScope.launch {
            mutableState.value = SystemStatusScreenState.Loading
            try {
                mutableState.value =
                    SystemStatusScreenState.Content(getSystemStatus.fetch().databaseReady)
            } catch (exception: CancellationException) {
                throw exception
            } catch (_: Exception) {
                mutableState.value = SystemStatusScreenState.Error("Unable to load system status.")
            }
        }
    }

    override fun onCleared() {
        getSystemStatus.close()
    }
}
