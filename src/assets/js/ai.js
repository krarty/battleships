/**
 * @brief   Websocket AI
 * @param   {string} host: hostname
 * @param   {string} port: port
 * @param   {function} onInit: callback on init
 * @param   {function} onMessage: callback on message
 * @param   {function} onClose: callback on disconnect
 */
export default (onInit = undefined, onMessage = undefined, onClose = undefined) => {

    let proto = 'ws'
    let host = 'localhost'
    let port = 8765

    if (process.env.NODE_ENV === 'production') {
        proto = 'wss'
        host = 'https://battleships-ai.herokuapp.com/'
        port = 443
    }

    const ws = new WebSocket(`${proto}://${host}:${port}`)

    ws.onopen = () => {

        console.debug(`[WS] Connected to ${host}:${port}`)

        ws.onmessage = (e) => {

            const msg = JSON.parse(e.data)

            console.debug('[WS] Received message', msg)

            if (onMessage !== undefined)
                onMessage(ws, msg)

        }

        ws.onclose = (e) => {

            console.debug('[WS] Connection closed', e)
            
            if(onClose !== undefined) 
                onClose(ws)
        
        }

        if (onInit !== undefined)
            onInit(ws)

    }

    ws.onerror = (e) => {

        console.debug('[WS] Error', e)

        if (onClose !== undefined)
            onClose(ws)
            
    }

}