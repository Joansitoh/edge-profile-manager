import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('electron', {
  ipcRenderer: {
    send: (channel, ...args) => ipcRenderer.send(channel, ...args),
    on: (channel, callback) =>
      ipcRenderer.on(channel, (event, ...args) => callback(event, ...args)),
    once: (channel, callback) =>
      ipcRenderer.once(channel, (event, ...args) => callback(event, ...args)),
    removeAllListeners: (channel) => ipcRenderer.removeAllListeners(channel),
    removeListener: (channel, callback) => ipcRenderer.removeListener(channel, callback)
  }
})
