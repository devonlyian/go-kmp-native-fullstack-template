package com.example.template.shared.feature.system.data

import com.example.template.shared.feature.system.domain.SystemStatus
import com.sun.net.httpserver.HttpServer
import java.net.InetSocketAddress
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlinx.coroutines.test.runTest

class ApolloSystemStatusRepositoryTest {
    @Test
    fun mapsReadyResponse() =
        withServer("""{"data":{"systemStatus":{"databaseReady":true}}}""") {
            assertEquals(SystemStatus(true), it.get())
        }

    @Test
    fun mapsNotReadyResponse() =
        withServer("""{"data":{"systemStatus":{"databaseReady":false}}}""") {
            assertEquals(SystemStatus(false), it.get())
        }

    @Test
    fun rejectsGraphQLErrors() =
        withServer("""{"errors":[{"message":"unavailable"}]}""") {
            assertFailsWith<Exception> { it.get() }
        }

    @Test
    fun rejectsPartialDataWithErrors() =
        withServer(
            """{"data":{"systemStatus":{"databaseReady":true}},"errors":[{"message":"partial failure"}]}"""
        ) {
            assertFailsWith<Exception> { it.get() }
        }

    @Test
    fun rejectsMalformedResponse() =
        withServer("not JSON") {
            assertFailsWith<Exception> { it.get() }
        }

    @Test
    fun rejectsHttpFailure() =
        withServer("unavailable", 503) {
            assertFailsWith<Exception> { it.get() }
        }

    private fun withServer(
        body: String,
        status: Int = 200,
        block: suspend (ApolloSystemStatusRepository) -> Unit,
    ) = runTest {
        val server = HttpServer.create(InetSocketAddress("127.0.0.1", 0), 0)
        server.createContext("/graphql") { exchange ->
            exchange.responseHeaders.add("Content-Type", "application/json")
            exchange.sendResponseHeaders(status, body.toByteArray().size.toLong())
            exchange.responseBody.use { it.write(body.toByteArray()) }
        }
        server.start()
        val repository =
            ApolloSystemStatusRepository("http://127.0.0.1:${server.address.port}/graphql")
        try {
            block(repository)
        } finally {
            repository.close()
            server.stop(0)
        }
    }
}
