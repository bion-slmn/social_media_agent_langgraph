import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import SocialMediaAgent from './components/SocialMediaAgent.jsx'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <SocialMediaAgent />

      </div>
    </>
  )
}

export default App
