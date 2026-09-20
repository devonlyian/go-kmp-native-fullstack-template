package com.example.template.shared.feature.system.domain

interface SystemStatusRepository {
    @Throws(Exception::class) suspend fun get(): SystemStatus

    fun close()
}
