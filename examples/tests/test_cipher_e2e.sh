#!/bin/sh

TMP_DIR="/tmp/tmp_cipher"

INPUT_FILE_CONTENT="test"
INPUT_FILE_NAME="test.txt"
INPUT_FILE_PATH="${TMP_DIR}/${INPUT_FILE_NAME}"

BACKEND_HOST="backend"
BACKEND_PORT=8080

PROXY_HOST="cipher"
PROXY_PORT=8080
PROXY_API="http://${PROXY_HOST}:${PROXY_PORT}/api/store"

STORAGE_PATH="/opt/storage"

# Util functions
failIfStorageNotEmpty() {
  [ -z "$(ls -A ${STORAGE_PATH})" ] || fail "error: ${STORAGE_PATH} is not empty!"
}

deleteUploadedFile() {
  rm -rf ${STORAGE_PATH}/${INPUT_FILE_NAME}
}
# ------------------------------------------------------------------------------

# Setup section
oneTimeSetUp() {
  deleteUploadedFile
  mkdir -p $TMP_DIR
  echo $INPUT_FILE_CONTENT > $INPUT_FILE_PATH
}

setUp() {
  failIfStorageNotEmpty
}
# ------------------------------------------------------------------------------

# Tests section
testDownloadFailsWhenFileHasNeverBeenUploaded() {
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" ${PROXY_API}/${INPUT_FILE_NAME})
  assertEquals 404 ${HTTP_STATUS}
}

testUpload() {
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST -F "file=@${INPUT_FILE_PATH}" ${PROXY_API}/)
  assertEquals 200 ${HTTP_STATUS}
}

testUploadedFileIsBiggerThanInputFile() {
  curl -s -X POST -F "file=@${INPUT_FILE_PATH}" ${PROXY_API}/
  STORED_SIZE=$(stat -c %s ${STORAGE_PATH}/${INPUT_FILE_NAME})
  assertTrue "[ ${STORED_SIZE} -gt ${#INPUT_FILE_CONTENT} ]"
}

testDownloadAfterUploadSucceedsFromProxy() {
  curl -s -X POST -F "file=@${INPUT_FILE_PATH}" ${PROXY_API}/
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" ${PROXY_API}/${INPUT_FILE_NAME})
  assertEquals 200 ${HTTP_STATUS}
}

testDownloadAfterUploadRetrievesUnencryptedFile() {
  curl -s -X POST -F "file=@${INPUT_FILE_PATH}" ${PROXY_API}/
  CONTENT=$(curl -s ${PROXY_API}/${INPUT_FILE_NAME})
  assertEquals ${INPUT_FILE_CONTENT} ${CONTENT}
}
# ------------------------------------------------------------------------------

# Tear-down section
tearDown() {
  deleteUploadedFile
}

oneTimeTearDown() {
  rm -rf ${TMP_DIR}
  failIfStorageNotEmpty
}
# ------------------------------------------------------------------------------

. shunit2
