#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${SONAR_TOKEN:-}" ]]; then
  echo "::error::SONAR_TOKEN must be provided from a GitHub secret."
  exit 2
fi

if [[ ! "${SONAR_HOST_URL:-}" =~ ^https?://[^[:space:]]+$ ]]; then
  echo "::error::SONAR_HOST_URL must be an HTTP(S) URL."
  exit 2
fi

if [[ ! "${SONAR_QUALITY_GATE_TIMEOUT:-}" =~ ^[1-9][0-9]*$ ]]; then
  echo "::error::SONAR_QUALITY_GATE_TIMEOUT must be a positive number of seconds."
  exit 2
fi

if [[ ! -f ./gradlew ]]; then
  echo "::error::No Gradle wrapper found in $(pwd). Set working-directory to the project root."
  exit 2
fi

pull_request_values=(
  "${SONAR_PULL_REQUEST_KEY:-}"
  "${SONAR_PULL_REQUEST_BRANCH:-}"
  "${SONAR_PULL_REQUEST_BASE:-}"
)
configured_pull_request_values=0
for value in "${pull_request_values[@]}"; do
  if [[ -n "$value" ]]; then
    ((configured_pull_request_values += 1))
  fi
done

if (( configured_pull_request_values != 0 && configured_pull_request_values != 3 )); then
  echo "::error::Set all three SonarQube pull-request inputs or leave all three empty."
  exit 2
fi

gradle_args=(
  --no-daemon
  --stacktrace
  sonar
  -Dsonar.qualitygate.wait=true
  "-Dsonar.qualitygate.timeout=${SONAR_QUALITY_GATE_TIMEOUT}"
)

if [[ -n "${SONAR_PROJECT_KEY:-}" ]]; then
  gradle_args+=("-Dsonar.projectKey=${SONAR_PROJECT_KEY}")
fi

if (( configured_pull_request_values == 3 )); then
  gradle_args+=(
    "-Dsonar.pullrequest.key=${SONAR_PULL_REQUEST_KEY}"
    "-Dsonar.pullrequest.branch=${SONAR_PULL_REQUEST_BRANCH}"
    "-Dsonar.pullrequest.base=${SONAR_PULL_REQUEST_BASE}"
  )
fi

./gradlew "${gradle_args[@]}"
