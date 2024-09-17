import { useState } from 'react'
import logo from '../assets/img/logo.png'

const ProfileCard = ({ profile, onClick }) => {
  const [profileName, setProfileName] = useState(
    profile.shortcut_name ? profile.shortcut_name : profile.name
  )

  return profile.id === '-1' ? (
    <div className="border border-dashed border-gray-400 profile-container py-4" onClick={onClick}>
      <input
        type="text"
        placeholder="Profile name"
        value="Add"
        className="rounded-t-lg text-center"
        readOnly
      />
      <div className="w-20 h-20 bg-gray-800 rounded-full">
        <img src={logo} className="w-full h-full" alt="logo" />
      </div>
    </div>
  ) : (
    <div className="border border-gray-400/50 profile-container py-4" onClick={onClick}>
      <input
        type="text"
        placeholder="Profile name"
        value={profileName}
        className="rounded-t-lg text-center"
        /* onChange={(e) => setProfileName(e.target.value)}
        onBlur={() =>
          window.electron.ipcRenderer.send(
            'modify-profile-name',
            profile.shortcut_name,
            profileName
          )
        } */
        readOnly
        /* onClick={(e) => e.stopPropagation()} */
      />
      <div className="w-20 h-20 bg-gray-800 rounded-full">
        <img src={logo} className="w-full h-full" alt="logo" />
      </div>
    </div>
  )
}

export default ProfileCard
