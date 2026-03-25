#!/bin/sh
set -eu

USER_NAME="${1:-user}"
CONFIG="/etc/doas.conf"

RULES=$(cat <<EOF
permit nopass ${USER_NAME} cmd /usr/bin/pkill
permit nopass ${USER_NAME} cmd /usr/bin/tor
permit nopass ${USER_NAME} cmd /usr/sbin/openvpn
EOF
)

tmp="$(mktemp)"
if [ -f "$CONFIG" ]; then
    cat "$CONFIG" > "$tmp"
fi

echo "$RULES" | while IFS= read -r rule; do
    [ -z "$rule" ] && continue
    grep -qxF "$rule" "$tmp" || echo "$rule" >> "$tmp"
done

doas sh -c "cat '$tmp' > '$CONFIG'"
rm -f "$tmp"
