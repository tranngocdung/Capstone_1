import { useState, useEffect } from "react";
import { useDispatch, useSelector } from 'react-redux';
import { getReviews } from "../../action/restaurant";
import img from '../../assets/images/empty.png'

function Review() {
    const reviews = useSelector(state=>state.restaurant.reviews);
    const dispatch = useDispatch();
    const RATING = [
        "★☆☆☆☆",
        "★★☆☆☆",
        "★★★☆☆",
        "★★★★☆",
        "★★★★★"
    ];

    useEffect(()=>{
        async function getreviews(){
            console.log(localStorage.getItem('rid'))
            const action  = await getReviews(localStorage.getItem('rid'))
            dispatch(action);
        }
        getreviews();
    }, [])

    return ( 
        <div>
            <nav className='nav-header'>
                <i class="fas fa-list"></i>
                <i class="fa-solid fa-user"></i>
            </nav>
            <nav className='nav-middle'>
            <div className="view-link">
                    <p className='top'>Reviews</p>
                    <p><a href="/restaurant">Home</a></p>
                    <i class="fas fa-chevron-right"></i>
                    <p>Reviews</p>
                </div>
                <div className="add-review">
                    
                </div>
            </nav>
            <div className="card table-responsive">
                <table id="result_list" class="table table-striped">
                    <thead>
                        <tr>
                            <th class="sorting" tabIndex="0" rowSpan="1" colSpan="1">
                                <div class="text">
                                    <b href="#">User</b>
                                </div>
                            </th>
                            <th class="sorting" tabIndex="0" rowSpan="1" colSpan="1">
                                <div class="text">
                                    <b href="#">Email</b>
                                </div>
                            </th>
                            <th class="sorting" tabIndex="0" rowSpan="1" colSpan="1">
                                <div class="text">
                                    <b href="#">Review</b>
                                </div>
                            </th>
                            <th class="sorting" tabIndex="0" rowSpan="1" colSpan="1">
                                <div class="text">
                                    <b href="#">Rating</b>
                                </div>
                            </th>
                            <th class="sorting" tabIndex="0" rowSpan="1" colSpan="1">
                                <div class="text">
                                    <b href="#">Date</b>
                                </div>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {reviews&&reviews.length>0? reviews.map((item, index)=>{
                            return (
                                <tr role="row" class="even" key={index}>
                                    <th>{item.user.username}</th>
                                    <td>{item.user.email}</td>
                                    <td>{item.review}</td>
                                    <td>{RATING[item.rating - 1]}</td>
                                    <td>{item.date.substring(0,10)}</td>
                                </tr>
                            )
                        })
                        : <tr role="row">
                            <td colSpan={7} className="text-center">
                                <img src={img}/>
                                <h6 className="text-secondary">No data</h6>
                            </td>
                            </tr>}
                    </tbody>
                </table>
            </div>
        </div>
     );
}

export default Review;