import React, {useState, useEffect} from "react"; 
import axios from "axios";
import Popup from "./Popup";
import "./style.css";
import '../../node_modules/font-awesome/css/font-awesome.min.css'; 
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faFile} from '@fortawesome/fontawesome-free-solid'

export default function Exercise({isOpen, filename}) {
  const [IsOpenp, setIsOpenp] = useState(isOpen);
  const [isOpen1, setIsOpen] = useState(false);
  const [child, setChild] = useState([]);
  const [name, setName] = useState();
  const [another, setAnother] = useState("");
  const [isActive, setIsActive] = useState(false);
  const [isActive1, setIsActive1] = useState(false);
  const [isOnclick, setIsOnclick] = useState("");
  const [text, setText] = useState("");

  const changeHandler = (e) => {
		setName(e.target.value)
	}

  const handleClick = () => {
    setIsOpen(!isOpen);
    setIsActive(current => !current);
  }

  const handleClick1 = () => {
    setIsActive1(current => !current);
  }
  const handleClick2 = () => {
    
  }

  const togglePopup = () => {
    setIsOpenp(!IsOpenp);
  }

  const getChild = (filename) => {
    var new1 = []
    axios.get('http://localhost:5000/' + filename)
    .then(res => {
        const elems = res.data
        for (let i=0; i<=elems.length; i++){
          if (elems[i].split(".")[1] === 'txt'){
            setAnother(elems[i])
          }
          else{
            new1.push(elems[i])
          }
          setChild(new1)
        }
    })
  }
  const getChild1 = (filename) => {
    axios.get('http://localhost:5000/' + filename)
    .then(res => {
        const elems = res.data
        setText(elems)
        
    })
  }

  const submit = (e) => {
		const data = new FormData() 
    data.append('name', filename + "/" + name)
		e.preventDefault()

		axios.post('http://127.0.0.1:5000/add', data,  {})	
		.then(() => {
			getChild(filename)
		})	
		.catch(error => console.error(error))
	}

  useEffect(() => {
    getChild(filename)
}, [filename]);

  return (
    <div>
      <i className="fa fa-plus"
        style={{
          display: isActive ? 'none' : '',
          color: 'green',
          padding: '25px 25px',
          fontSize: '37px',
        }}
       
        onClick={setIsOpenp}></i>
         <i className="fa-solid fa-backward"
        style={{
          display: isActive ? 'none' : '',
          color: 'red',
          padding: '25px 25px',
          fontSize: '37px',
        }}
       
        onClick={handleClick2}></i>
        <br/>
        {IsOpenp && <Popup
          content={<>
            <div>
              <label>Folder name</label>
              <br/>
              <input
                type="text"
                name="name"
                value={name}
                onChange={changeHandler}
              />
              </div>
              <div>
                  <button type="submit" onClick={(e)=>submit(e)}>Submit</button>
              </div>
        </>}
        handleClose={togglePopup}
        />}
      {child.map((el, i) => 
      <i className="fa fa-folder" aria-hidden="true"
      style={{
        display: isActive ? 'none' : '',
        color: 'black',
        padding: '35px 55px',
        textAlign: 'center',
        margin: '14px 27px',
        fontSize: '67px',
      }} 
      onClick={() => {handleClick(); setIsOnclick(child[i])}}><p
      style={{
        color: 'black',
        textAlign: 'center',
        fontSize: '17px',
      }}>{child[i]}</p></i>
      
      )}
      {another !== ""  && 
        <FontAwesomeIcon icon={faFile}
        style={{
          display: isActive ? 'none' : '',
          color: 'blue',
          padding: '35px 55px',
          textAlign: 'center',
          margin: '14px 27px',
          fontSize: '67px',
        }} 
        onClick={() => {handleClick1()}}>
          <p>{another}</p>
        {console.log(another)}
        </FontAwesomeIcon>
      }
      {isActive1 && getChild1(filename+ "/" + another)}
      {text !== "" && <p>{text}</p>}

      {isOpen1 && <Exercise isOpen={isOpen} filename={filename + "/" + isOnclick}/>}
    </div>
)
}