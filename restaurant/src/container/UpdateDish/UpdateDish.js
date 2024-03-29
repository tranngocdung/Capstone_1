import {NavLink, useParams, useNavigate} from 'react-router-dom'
import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { detailDish, getCategory, updateDish } from '../../action/restaurant';
import { UPDATE_DISH } from '../../action/type';


function UpdateDish() {
    const rid = "res51312ab1b4";
    const dish = useSelector(state=>state.restaurant.dish);
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const category = useSelector(state=>state.restaurant.category);
    const {did} = useParams();
    const [form, setForm] = useState({
        title: "",
        image: null,
        description: "",
        price: 0,
        old_price: 0,
        product_status: "draft",
        specifications: "",
        featured: false,
        digital: false,
        cid: ""
    });

    useEffect(()=>{
        async function getcategory(){
            const action = await getCategory(rid)
            dispatch(action);
        }
        getcategory();

        async function getDetailDish(){
            const action = await detailDish(did, form);
            dispatch(action);
        }
        getDetailDish();
    }, [])

    useEffect(()=>{
        async function getDetailDish(){
            const action = await detailDish(did, form);
            dispatch(action);
        }
        getDetailDish();
    }, [])

    function checkInput(){
        if(form.title === ""){
            alert("Please input Title!");
            return false;
        }else if(form.description === ""){
            alert("Please input description!");
            return false;
        }else if(form.cid === ""){
            alert("Please choice Category!");
            return false;
        }return true;
    }

    useEffect(()=>{
        form.title = dish.title;
        form.description= dish.description;
        form.price= dish.price;
        form.old_price= dish.old_price;
        form.product_status= dish.product_status;
        form.specifications= dish.specifications;
        form.featured= dish.featured;
        form.digital= dish.digital;
        form.cid = dish.category?dish.category.cid: "";
    }, [dish])

    function handelChange(e){
        setForm({...form, [e.target.name]: e.target.value});
    }

    function handelChoice(e){
        let file = e.target;
        if(file.files &&file.files[0]){
            setForm({...form, ['image']: file.files[0]});
        }
    }

    function handelCheck(e){
        setForm({...form, [e.target.name]: e.target.checked});
    }

    async function handelsubmit(e){
        e.preventDefault();
        if(checkInput()){
            const action = await updateDish(did, form);
            console.log(action);
            dispatch(action);
            if(action.type === UPDATE_DISH){
                navigate("/restaurant/dish");
            }
        }
    }
    return ( 
        <div class="content">
            <nav className='nav-header'>
                <i class="fas fa-list"></i>
                <i class="fa-solid fa-user"></i>
            </nav>
            <nav className='nav-middle'>
                <div className="view-link">
                    <p className='top'>The Dishes</p>
                    <p><a href="/restaurant">Home</a></p>
                    <i class="fas fa-chevron-right"></i>
                    <p><NavLink to="/restaurant/dish">The Dishes</NavLink></p>
                    <i class="fas fa-chevron-right"></i>
                    <p>Update Dish</p>
                </div>
                <div className="add-dish">
                    
                </div>
            </nav>
            <div class="container-fluid">
                <section class="content">
                    <div class="row">
                        <div id="content-main">
                                <input type="hidden"/>
                                <div class="row">
                                    <div class="col-12 col-lg-9">
                                        <div class="card">
                                            <div class="card-body">
                                                <div class="form-group field-did">
                                                    <div class="row">
                                                        <label class="col-sm-3 text-left" for="id_did">
                                                            Did
                                                            <span class="text-red">* </span> 
                                                        </label>
                                                        <div class=" col-sm-7 field-did ">
                                                            <input className="input" type="text" name="did" value={dish.did} maxlength="20" disabled/>
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="form-group field-title">
                                                    <div class="row">
                                                        <label class="col-sm-3 text-left">
                                                            Title
                                                            <span class="text-red">* </span>  
                                                        </label>
                                                        <div class=" col-sm-7 field-title">
                                                            <input onChange={handelChange} value={form.title} className="input" type="text" name="title"/>
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="form-group field-image">
                                                    <div class="row">
                                                        <label class="col-sm-3 text-left">
                                                            Image
                                                            <span class="text-red">* </span>
                                                        </label>
                                                        <div class=" col-sm-7 field-image">
                                                            <input onChange={handelChoice} type="file" name="image"/>
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="form-group field-description">
                                                    <div class="row">
                                                        <label class="col-sm-3 text-left">
                                                            Description
                                                        </label>
                                                        <div class=" col-sm-7 field-description">
                                                            <textarea onChange={handelChange} value={form.description} type="number" name="description" rows="5"/>
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="form-group field-price">
                                                    <div class="row">
                                                        <label class="col-sm-3 text-left">
                                                            Price
                                                            <span class="text-red">* </span>
                                                        </label>
                                                        <div class=" col-sm-7 field-price">
                                                            <input onChange={handelChange} value={form.price} className="input" type="number" name="price"/>
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="form-group field-old_price">
                                                    <div class="row">
                                                            <label class="col-sm-3 text-left">
                                                                Old price
                                                                <span class="text-red">* </span>
                                                            </label>
                                                            <div class="col-sm-7 field-old_price">
                                                                <input onChange={handelChange} value={form.old_price} className="input" type="number" name="old_price"/>
                                                            </div>
                                                    </div>
                                                </div>
                                                <div class="form-group field-product_status">
                                                    <div class="row">
                                                        <label class="col-sm-3 text-left">
                                                            Product status
                                                            <span class="text-red">* </span>
                                                        </label>
                                                        <div class="col-sm-7 field-product_status">
                                                            <select onChange={handelChange} value={form.product_status} className="input" name="product_status">
                                                                <option value="draft" data-select2-id="select2-data-2-4k8x">Draft</option>
                                                                <option value="disabled">Disabled</option>
                                                                <option value="rejected">Rejected</option>
                                                                <option value="in_review">In review</option>
                                                                <option value="published">Published</option>
                                                            </select>
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="form-group field-featured">
                                                    <div class="row">
                                                        <label class="col-sm-3 text-left">
                                                            Featured
                                                        </label>
                                                        <div class="col-sm-7 field-featured">
                                                            <input onChange={handelCheck} checked={form.featured} type="checkbox" name="featured"/>
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="form-group field-digital">
                                                    <div class="row">   
                                                        <label class="col-sm-3 text-left">
                                                            Digital
                                                        </label>
                                                        <div class="col-sm-7 field-digital">
                                                            <input onChange={handelCheck} checked={form.digital} type="checkbox" name="digital"/>
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="form-group field-category">
                                                    <div class="row">
                                                        <label class="col-sm-3 text-left" for="id_category">
                                                            Category
                                                            <span class="text-red">* </span>
                                                        </label>
                                                        <div class="col-sm-7 field-category">
                                                            <div class="related-widget-wrapper" >
                                                                <select value={form.cid} onChange={handelChange} className="input" name="cid">
                                                                    <option value="" selected="">---------</option>
                                                                    {category?category.map((item, index)=>{
                                                                        return (
                                                                            <option key={index} value={item.cid}>{item.title}</option>
                                                                        )
                                                                    }):""}
                                                                </select>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-12 col-lg-3">
                                        <div class="form-group">
                                            <input onClick={handelsubmit} type="submit" value="Save" class="btn btn-success form-control"/>
                                        </div>
                                    </div>
                                </div>
                        </div>
                    </div>
                </section>
            </div>
        </div>
     );
}

export default UpdateDish;