import React, {useState} from 'react'
import axios from 'axios'
import Popup from './Popup'
import "./style.css";

function PostForm({getElem, isOpen}) {
	const [IsOpen, setIsOpen] = useState(isOpen);
	const [selectedFile, setSelectFile] = useState('');
	const [FirstName, setFirstName] = useState('');
	const [LastName, setLastName] = useState('');
	const [height, setHeight] = useState();

	const togglePopup = () => {
 		setIsOpen(!IsOpen);
 	}

	const handleInputChange = (event) => {
		let reader = new FileReader()
        reader.readAsDataURL(event.target.files[0])
        reader.onload = () => {
            setSelectFile(event.target.files[0])
        }
		console.log(selectedFile)
	}

	const changeHandler = (e) => {
		setFirstName(e.target.value)
	}

	const changeHandler1 = (e) => {
		setLastName(e.target.value)
	}

	const changeHandler2 = (e) => {
		setHeight(e.target.value)

	}

	const submit = (e) => {
		const data = new FormData() 
        data.append('photo', selectedFile)
        data.append('FirstName', FirstName)
        data.append('LastName', LastName)
        data.append('height', height)

		e.preventDefault()

		axios.post('http://127.0.0.1:5000/add', data, {})	
		.then(() => {
			getElem()
		})	
		.catch(error => console.error(error))
	}
	
	return (<div>
				{IsOpen && <Popup
					content={<>
						<div>
						<div>
							<input
								type="file"
								name="photo"
								onChange= {handleInputChange}
							/>
						</div>
						<div>
							<input
								type="text"
								name="FirstName"
								value={FirstName}
								onChange={changeHandler}
							/>
						</div>
						<div>
							<input
								type="text"
								name="LastName"
								value={LastName}
								onChange={changeHandler1}
							/>
						</div>
						<div>
							<input
								type="text"
								name="height"
								value={height}
								onChange={changeHandler2}
							/>
						</div>
						<button type="submit" onClick={(e)=>submit(e)}>Submit</button>
					</div>
					</>}
					handleClose={togglePopup}
					/>}
					</div>
				)
}
export default PostForm

