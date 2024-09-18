import { useEffect, useRef, useState } from 'react'
import './assets/main.css'

import logo from './assets/img/logo.png'
import background from './assets/img/background.png'

import ProfileCard from './components/ProfileCard'

function App() {
  const [profiles, setProfiles] = useState([])
  const [closeOnLaunch, setCloseOnLaunch] = useState(false)

  useEffect(() => {
    window.electron.ipcRenderer.on('fetched-profiles', (event, profiles) => setProfiles(profiles))
    window.electron.ipcRenderer.on('close-on-select', (event, state) => setCloseOnLaunch(state))
    window.electron.ipcRenderer.send('fetch-profiles')
    window.electron.ipcRenderer.send('close-on-select')

    return () => {
      window.electron.ipcRenderer.removeAllListeners('fetched-profiles')
      window.electron.ipcRenderer.removeAllListeners('close-on-select')
    }
  }, [])

  const handleStartProfile = (profile) => {
    window.electron.ipcRenderer.send('launch-profile', profile.folder)
  }

  const handleAddProfile = () => {
    window.electron.ipcRenderer.send('add-profile')
  }

  const handleLaunchInprivate = () => {
    window.electron.ipcRenderer.send('launch-inprivate')
  }

  const handleToggleCloseOnLaunch = () => {
    window.electron.ipcRenderer.send('toggle-close-on-select')
  }

  return (
    <div
      className="h-screen w-full flex flex-col justify-between px-10"
      style={{
        backgroundImage: `url(${background})`,
        backgroundSize: 'cover',
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'center'
      }}
    >
      <section className="flex flex-col justify-center items-center mt-10 gap-3 h-full">
        <img src={logo} width={35} alt="logo" className="mb-2" />
        <h1 className="text-3xl font-base">Who's using Edge?</h1>
        <p className="text-md text-gray-400 text-center max-w-lg xl:max-w-3xl">
          With Edge profiles you can separate all your Edge stuff. Create profiles for friends and
          family, or split between work and fun.
        </p>
        <div className="grid grid-cols-3 xl:grid-cols-4 gap-4 overflow-y-auto overflow-x-hidden pr-2 h-[50%]">
          {profiles.map((profile) => {
            return (
              <ProfileCard
                profile={profile}
                onClick={() => handleStartProfile(profile)}
                closeOnLaunch={closeOnLaunch}
              />
            )
          })}
          <ProfileCard
            profile={{
              name: 'Add',
              checked: false,
              id: '-1'
            }}
            onClick={handleAddProfile}
          />
        </div>
      </section>
      <div className="flex justify-between h-20 p-4 px-10">
        {/* LEFT SIDE */}
        <div>
          <button
            className="border border-gray-500 bg-transparent rounded-md px-8 py-1 flex items-center justify-center gap-2 text-blue-300"
            onClick={handleLaunchInprivate}
          >
            {/* <FaUserCircle className="text-xl" /> */}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 512 512"
              fill="currentColor"
              className="h-4 text-blue-300"
            >
              <path d="M399 384.2C376.9 345.8 335.4 320 288 320l-64 0c-47.4 0-88.9 25.8-111 64.2c35.2 39.2 86.2 63.8 143 63.8s107.8-24.7 143-63.8zM0 256a256 256 0 1 1 512 0A256 256 0 1 1 0 256zm256 16a72 72 0 1 0 0-144 72 72 0 1 0 0 144z" />
            </svg>
            <p className="text-sm font-semibold">Guest mode</p>
          </button>
        </div>

        {/* RIGHT SIDE (checkbox with text) */}
        <div className="flex items-center gap-2">
          <input
            type="checkbox"
            id="checkbox"
            name="checkbox"
            value="checkbox"
            className="w-3 h-3"
            checked={closeOnLaunch}
            onClick={handleToggleCloseOnLaunch}
          />
          <label htmlFor="checkbox" className="text-gray-400 text-sm">
            Close on selection
          </label>
        </div>
      </div>
    </div>
  )
}

export default App
