import React, {useState} from 'react'
import axios from 'axios'
import Popup from './Popup'
import "./style.css";

function PutForm({getElem, id, FirstName, LastName, height, photo }){
	const [id1] = useState(id);
	const [isOpen, setIsOpen] = useState(true);
	const [photo1, setPhoto] = useState(photo)
	const [FirstName1, setFirstName] = useState(FirstName);
	const [LastName1, setLastName] = useState(LastName);
	const [height1, setHeight] = useState(height);
	const [mind, setMind] = useState(0)

	const togglePopup = () => {
		setIsOpen(!isOpen);
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

	const changeHandler3 = (e) => {
		let reader = new FileReader()
        reader.readAsDataURL(e.target.files[0])
        reader.onload = () => {
            setPhoto(e.target.files[0])
			setMind(1)
        }
		console.log(photo)
	}
	
	const submit1 = (e, id) => {
		const data1 = new FormData() 
		data1.append('photo', photo1)
		console.log(photo1)
		e.preventDefault()

		axios.put('http://127.0.0.1:5000/update/' + id + "/photo", data1, {})	
		.then(() => {
			getElem()
		})	
		.catch(error => console.error(error))
	}

	const submit = (e, id) => {
		mind === 1 ? submit1(e, id) : <div></div>
		const data = new FormData() 
        data.append('FirstName', FirstName1)
        data.append('LastName', LastName1)
        data.append('height', height1)

		e.preventDefault()

		axios.put('http://127.0.0.1:5000/update/' + id, data, {})	
		.then(() => {
			getElem()
		})	
		.catch(error => console.error(error))
	}

	return (<div>
				{isOpen && <Popup
				content={<>
					<div>
					<img src={"/imag/"  + photo1} alt=""/>
						<div>
							<input
								type="file"
								name="photo1"
								onChange={changeHandler3}
							/>
						</div>
						<div>
							<input
								type="text"
								name="FirstName1"
								value={FirstName1}
								onChange={changeHandler}
							/>
						</div>
						<div>
							<input
								type="text"
								name="LastName1"
								value={LastName1}
								onChange={changeHandler1}
							/>
						</div>
						<div>
							<input
								type="text"
								name="height1"
								value={height1}
								onChange={changeHandler2}
							/>
						</div>
						<button type="submit" onClick={(e)=>submit(e, id1)}>Update</button>
					</div>
					</>}
					handleClose={togglePopup}
					/>}
				</div>
			)
}
export default PutForm
