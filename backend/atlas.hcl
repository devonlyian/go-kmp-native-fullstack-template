env "local" {
  src = "file://db/schema"
  dev = "docker://postgres/18.6/dev"
  url = getenv("DATABASE_URL")
  migration {
    dir = "file://db/migration"
  }
}
