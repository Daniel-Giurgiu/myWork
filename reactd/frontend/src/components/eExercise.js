import React, {useState, useEffect} from "react"; 

export default function FriendStatus() {
  const [resourceType, setResourceType] = useState('posts');
  
  useEffect(() => {
    console.log('resource changed')
    return () => {
      console.log('onMount')
    }
  }, [resourceType])
  return(
    <>
    <div>
      <button onClick={() => setResourceType('post')}>Posts</button>
      <button onClick={() => setResourceType('users')}>Users</button>
      <button onClick={() => setResourceType('comments')}>Comments</button>
    </div>
    <h1>{resourceType}</h1>
    </>
  )
}
// export default function FriendStatus() {
//   const [windowWidth, setwindowWidth] = useState(window.innerWidth)
//   const handleReseize = () => {
//     setwindowWidth(window.innerWidth)
//   }
//   useEffect(() => {
//     window.addEventListener('resize', handleReseize)
//   }, [])
//   return (
//     <div>{windowWidth}</div>
//   )
// }