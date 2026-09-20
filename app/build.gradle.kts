import org.gradle.api.attributes.Bundling

plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.android.kotlin.multiplatform.library) apply false
    alias(libs.plugins.kotlin.multiplatform) apply false
    alias(libs.plugins.kotlin.compose) apply false
    alias(libs.plugins.apollo) apply false
}

val ktfmt =
    configurations.create("ktfmt") {
        attributes {
            attribute(Bundling.BUNDLING_ATTRIBUTE, objects.named(Bundling.SHADOWED))
        }
    }

dependencies { ktfmt("com.facebook:ktfmt:0.64") }

val kotlinSources =
    fileTree(projectDir) {
        include("**/*.kt", "**/*.kts")
        exclude("**/build/**", "**/.gradle/**", "**/.kotlin/**")
    }

for (check in listOf(false, true)) {
    tasks.register<JavaExec>(if (check) "checkKotlinFormat" else "formatKotlin") {
        group = "verification"
        classpath = ktfmt
        mainClass.set("com.facebook.ktfmt.cli.Main")
        args("--kotlinlang-style")
        if (check) args("--dry-run", "--set-exit-if-changed")
        args(kotlinSources.files.sorted().map { it.absolutePath })
    }
}
