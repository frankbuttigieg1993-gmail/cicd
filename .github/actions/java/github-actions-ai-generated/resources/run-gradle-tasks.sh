#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${GRADLE_TASKS:-}" ]]; then
  echo "::error::At least one Gradle task must be configured."
  exit 2
fi

read -r -a tasks <<< "$GRADLE_TASKS"
if (( ${#tasks[@]} == 0 )); then
  echo "::error::At least one Gradle task must be configured."
  exit 2
fi

if [[ ! -f ./gradlew ]]; then
  echo "::error::No Gradle wrapper found in $(pwd). Set working-directory to the project root."
  exit 2
fi

./gradlew --no-daemon --stacktrace "${tasks[@]}"
