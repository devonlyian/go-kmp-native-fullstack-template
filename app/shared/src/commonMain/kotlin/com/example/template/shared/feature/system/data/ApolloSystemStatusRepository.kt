package com.example.template.shared.feature.system.data

import com.apollographql.apollo.ApolloClient
import com.example.template.shared.feature.system.domain.SystemStatus
import com.example.template.shared.feature.system.domain.SystemStatusRepository
import com.example.template.shared.feature.system.network.SystemStatusQuery

class ApolloSystemStatusRepository(endpoint: String) : SystemStatusRepository {
    private val client = ApolloClient.Builder().serverUrl(endpoint).build()

    override suspend fun get(): SystemStatus {
        val response = client.query(SystemStatusQuery()).execute()
        check(response.errors.isNullOrEmpty()) { "GraphQL request failed" }
        val status = response.dataOrThrow().systemStatus
        return SystemStatus(databaseReady = status.databaseReady)
    }

    override fun close() = client.close()
}
