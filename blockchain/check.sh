RPC_URL="${SEPOLIA_RPC_URL:-https://rpc.ankr.com/eth_sepolia}"
ADDR="0xC541727abA1192AB5BC91D3489ED9683707724f4"

# replace with your INFURA_SEPOLIA_URL if different
RPC="${INFURA_SEPOLIA_URL:-https://sepolia.infura.io/v3/b84bd50caac64df888a86906631ba7fc}"

# simple request
curl -s -X POST "$RPC" -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' | jq

curl -s -X POST "$RPC_URL" -H "Content-Type: application/json" \
  --data "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getCode\",\"params\":[\"$ADDR\",\"latest\"],\"id\":1}" \
  | jq -r '.result'