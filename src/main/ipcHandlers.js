import { ipcMain, app } from 'electron'
import { exec } from 'child_process'
import path from 'path'
import fs from 'fs'
import Store from 'electron-store'

const store = new Store()

const registerIpcHandlers = () => {
  ipcMain.on('toggle-close-on-select', (event) => {
    store.set('closeOnSelect', !store.get('closeOnSelect'))
    event.sender.send('close-on-select', store.get('closeOnSelect'))
  })

  ipcMain.on('close-on-select', (event) => {
    event.sender.send('close-on-select', store.get('closeOnSelect'))
  })

  ipcMain.on('fetch-profiles', (event) => {
    const localAppData = process.env.LOCALAPPDATA

    const edgeBasePath = path.join(localAppData, 'Microsoft', 'Edge', 'User Data')
    const profileListPath = path.join(edgeBasePath, 'Local State')

    let profiles = []

    try {
      const data = JSON.parse(fs.readFileSync(profileListPath, 'utf-8'))

      for (const [key, value] of Object.entries(data.profile.info_cache)) {
        const profileFolder = path.join(edgeBasePath, key)
        const avatarPath = path.join(profileFolder, 'Google Profile Picture.png')

        profiles.push({
          name: value.name,
          shortcut_name: value.shortcut_name,
          username: value.user_name,
          folder: key,
          avatar: fs.existsSync(avatarPath) ? avatarPath : ''
        })
      }
    } catch (error) {
      console.error('Error on read profiles file:', error)
    }

    event.sender.send('fetched-profiles', profiles)
  })

  ipcMain.on('modify-profile-name', (event, oldName, newName) => {
    const localAppData = process.env.LOCALAPPDATA
    const edgeBasePath = path.join(localAppData, 'Microsoft', 'Edge', 'User Data')
    const profileListPath = path.join(edgeBasePath, 'Local State')

    if (!newName) {
      return
    }

    try {
      const data = JSON.parse(fs.readFileSync(profileListPath, 'utf-8'))

      for (const [key, value] of Object.entries(data.profile.info_cache)) {
        if (value.shortcut_name === oldName) {
          value.shortcut_name = newName
        } else if (value.name === oldName) {
          value.name = newName
        }
      }

      fs.writeFileSync(profileListPath, JSON.stringify(data, null, 2))
    } catch (error) {
      console.error('Error on replacing profile name:', error)
    }
  })

  ipcMain.on('add-profile', (event) => {
    const edgeExe = path.join(
      process.env['ProgramFiles(x86)'],
      'Microsoft',
      'Edge',
      'Application',
      'msedge.exe'
    )
    const cmdOptions = `--profile-directory="${'new'}"`
    let cmd = `"${edgeExe}" ${cmdOptions}`

    exec(cmd, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing command: ${error.message}`)
        return
      }
    })
  })

  ipcMain.on('launch-inprivate', (event) => {
    const edgeExe = path.join(
      process.env['ProgramFiles(x86)'],
      'Microsoft',
      'Edge',
      'Application',
      'msedge.exe'
    )
    const cmdOptions = `--inprivate`
    let cmd = `"${edgeExe}" ${cmdOptions}`

    exec(cmd, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing command: ${error.message}`)
        return
      }
    })

    if (store.get('closeOnSelect')) app.quit()
  })

  ipcMain.on('launch-profile', (event, profileName) => {
    const edgeExe = path.join(
      process.env['ProgramFiles(x86)'],
      'Microsoft',
      'Edge',
      'Application',
      'msedge.exe'
    )
    const cmdOptions = `--profile-directory="${profileName}"`
    let cmd = `"${edgeExe}" ${cmdOptions}`

    exec(cmd, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing command: ${error.message}`)
        return
      }
    })

    if (store.get('closeOnSelect')) app.quit()
  })
}

export { registerIpcHandlers }
