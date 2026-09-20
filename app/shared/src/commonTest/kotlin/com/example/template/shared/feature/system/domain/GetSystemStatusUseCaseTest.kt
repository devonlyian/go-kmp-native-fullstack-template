package com.example.template.shared.feature.system.domain

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertTrue

class GetSystemStatusUseCaseTest {
    @Test
    fun `returns repository status`() =
        kotlinx.coroutines.test.runTest {
            val useCase =
                GetSystemStatusUseCase(
                    object : SystemStatusRepository {
                        override suspend fun get() = SystemStatus(databaseReady = true)

                        override fun close() = Unit
                    }
                )

            assertEquals(SystemStatus(databaseReady = true), useCase.fetch())
        }

    @Test
    fun `preserves repository failure`() =
        kotlinx.coroutines.test.runTest {
            val failure = IllegalStateException("offline")
            val useCase =
                GetSystemStatusUseCase(
                    object : SystemStatusRepository {
                        override suspend fun get(): SystemStatus = throw failure

                        override fun close() = Unit
                    }
                )

            assertTrue(assertFailsWith<IllegalStateException> { useCase.fetch() } === failure)
        }
}
