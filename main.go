package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"golang.org/x/net/websocket"
)

var params Params
var user []*websocket.Conn

func init() {
	params = Params{
		WebSocketPort: ":9988",
		ApiPort: ":6721",
	}
}

func main() {
	fmt.Printf("Start\n")
	
	// ws
	go func(){
		mux := http.NewServeMux()
		mux.Handle("/ws", websocket.Handler(webSocket))
		http.ListenAndServe(params.WebSocketPort,mux)
	}()

	// api
	go func() {
		mux := http.NewServeMux()
		mux.Handle("/api", http.HandlerFunc(apiHandler))
		http.ListenAndServe(params.ApiPort,mux)
	}()

	fmt.Printf("Server start at %s\n", time.Now().String())

	select{}
}

/*
 Func to handle WebSocket Connection
 */
func webSocket(ws *websocket.Conn) {
	user = append(user, ws)
	select {}
}

/*
 send json message to web through WebSocket
 */
func sendMsg(msg string) {
	for _, v := range user {
		err := websocket.Message.Send(v, string(msg))
		if err != nil {
			fmt.Printf("%s 发送出错\n",time.Now().String())
		} else {
			fmt.Printf("%s 发送成功: %s\n", time.Now().String(), msg)
		}
	}
}

func apiHandler(w http.ResponseWriter, r *http.Request) {
	var req Req
	jsonDecoder := json.NewDecoder(r.Body)
	err := jsonDecoder.Decode(&req)
  if err != nil {
      fmt.Println(err.Error())
  }

	sendMsg(req.Content)
}

/*
 command-Line params struct
 */
type Params struct {
	WebSocketPort	string
	ApiPort 		string
}

/*
 json data struct
 */
type PostData struct {
	Nick	string	`json:"nick"`
	Type	string	`json:"type"`
	Message	string	`json:"message"`
	Time	string	`json:"time"`
}

type Req struct {
	Content string `json:"content"`
}