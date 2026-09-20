package com.example.template.shared.feature.system.domain

class GetSystemStatusUseCase(private val repository: SystemStatusRepository) {
    @Throws(Exception::class) suspend fun fetch(): SystemStatus = repository.get()

    fun close() = repository.close()
}
