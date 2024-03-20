/* ==================== RoomRequest ==================== */

class RoomRequest {
    #socket_url;
    #socket;

    constructor() {
        this.#socket_url = `ws://${window.location.host}/ws/home/`;
        this.#socket = new WebSocket(this.#socket_url);

        this.#socketListen();
    }


    // -------------- RECEIVE --------------

    #socketListen()
    {
        this.#socket.onmessage = (e) => {
            let data = JSON.parse(e.data);

            if (data["type"] === "room_action")
            {
                if (data["action"] === "add")
                    visual_addRoom(data);
                else if (data["action"] === "remove")
                    visual_removeRoom(data);
                else if (data["action"] === "player_join")
                    visual_editRoom(data);
            }
            else
            {
                console.log('Home Data:', data)
            }
        };
    }


    // -------------- SEND --------------

    createRoom()
    {
        this.#socket.send(JSON.stringify({
            type: "create_room",
            "ia_game": "none",
            player_id: player_id
        }))
    }

    joinRoom(room_id)
    {
        this.#socket.send(JSON.stringify({
            type: "join_room",
            room_id: room_id,
            player_id: player_id
        }))
    }
}