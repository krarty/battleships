/**
 * @brief   Websocket AI
 * @param   {string} host: hostname
 * @param   {string} port: port
 * @param   {function} onInit: callback on init
 * @param   {function} onMessage: callback on message
 * @param   {function} onClose: callback on disconnect
 */
export default (host, port, onInit = undefined, onMessage = undefined, onClose = undefined) => {

    const ws = new WebSocket(`${host === 'localhost' ? 'ws' : 'wss'}://${host}:${port}`)

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