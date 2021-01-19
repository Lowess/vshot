echo "📺 Xvfb Listening on :$DISPLAY"
Xvfb -ac -listen tcp $arg :$DISPLAY &

export DISPLAY=:$DISPLAY

echo "📷 Running Vshot"
python3 bin/vshot "$@"
