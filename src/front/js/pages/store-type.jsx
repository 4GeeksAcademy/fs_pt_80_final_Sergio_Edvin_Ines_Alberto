import React, { useContext, useEffect } from "react";
import { Context } from "../store/appContext.js";
import { useParams } from "react-router";
import { useNavigate } from "react-router-dom";
import "../../styles/store.css";

import { ProductCard } from "../component/product-small-card.jsx";
import { ProductBCard } from "../component/product-big-card.jsx"
import { VideogameCard } from "../component/videogame-small-card.jsx";
import { AllType } from "../component/all-type.jsx";
import { LoginModal } from "../component/login-modal.jsx";


export const CategoryPage = () => {
    const { store, actions } = useContext(Context);
    const { category } = useParams();
    const navigate = useNavigate();

    const handleCategoryClick = (category) => {
        navigate(`/store/${category}`);
    };

     useEffect(() => {
                    window.scrollTo(0, 0); 
                    actions.setShowLoginModal(false); 
                }, []);

    return (
        <div className="home-container">
            {store.showLoginModal && <LoginModal />}
            <div className="row d-flex justify-content-center my-5 icons-store">
                <figure className="col-4 col-lg-2">
                    <img src="https://res.cloudinary.com/dshjlidcs/image/upload/c_thumb,w_200,g_face/v1738527219/web-img/vhxp03yiac2oxegzcy9a.png" alt="Consolas" className={category == "consolas" ? "selected img-fluid" : "img-fluid "} onClick={() => handleCategoryClick("consolas")} />
                </figure>
                <figure className="col-4 col-lg-2">
                    <img src="https://res.cloudinary.com/dshjlidcs/image/upload/c_thumb,w_200,g_face/v1738527219/web-img/mufcnmnv4pcgs71dyhyc.png" alt="Videojuegos" className={category == "videojuegos" ? "selected img-fluid" : "img-fluid "} onClick={() => handleCategoryClick("videojuegos")} />
                </figure>
                <figure className="col-4 col-lg-2">
                    <img src="https://res.cloudinary.com/dshjlidcs/image/upload/v1738527219/web-img/ciyiiqpzbxoj2jn37kqu.png" alt="Accesorios" className={category == "accesorios" ? "selected img-fluid" : " img-fluid"} onClick={() => handleCategoryClick("accesorios")} />
                </figure>
            </div>
            <h3 className="t-seccion">{category}</h3>
            <section className="my-5">
                <div className="horizontal-scrollable">
                    <div className="row flex-nowrap pt-1">
                        {category === 'videojuegos' ? (
                            store[category]?.filter((item) => !item.promoted)
                                .map((item) => (
                                    <VideogameCard
                                        key={item.id}
                                        img={item.img}
                                        name={item.name}
                                        brand={item.brand}
                                        price={item.price}
                                        promoted={item.promoted}
                                        id={item.id}
                                    />
                                ))
                        ) : (
                            store[category]
                                ?.filter((item) => !item.promoted)
                                .map((item) => (
                                    <ProductCard
                                        key={item.id}
                                        img={item.img}
                                        name={item.name}
                                        brand={item.brand}
                                        price={item.price}
                                        promoted={item.promoted}
                                        id={item.id}
                                    />
                                ))
                        )}
                    </div>
                </div>
            </section>
            <div className="divider"></div>
            <section className="my-5">
                <div className="horizontal-scrollable">
                    <div className="row flex-nowrap pt-1">
                        {category === 'videojuegos' ? (
                            store.promoted
                                ?.filter((promo) => promo.category === category)
                                .map((promo) => (
                                    <VideogameCard
                                        key={promo.id}
                                        img={promo.img}
                                        name={promo.name}
                                        brand={promo.brand}
                                        price={promo.price}
                                        promoted={promo.promoted}
                                        id={promo.id}
                                    />
                                ))
                        ) : (
                            store.promoted
                                ?.filter((promo) => promo.category === category)
                                .map((promo) => (
                                    <ProductCard
                                        key={promo.id}
                                        img={promo.img}
                                        name={promo.name}
                                        brand={promo.brand}
                                        price={promo.price}
                                        promoted={promo.promoted}
                                        id={promo.id}
                                    />
                                ))
                        )}
                    </div>
                </div>
            </section>
            <div className="divider"></div>
            <section className="my-5">
                <div className="pt-1">
                    {store[category]
                        ?.filter((item) => item.promoted).sort(() => Math.random() - 0.5).slice(0, 1)
                        .map((item) => (
                            <ProductBCard
                                key={item.id}
                                img={item.img}
                                name={item.name}
                                brand={item.brand}
                                price={item.price}
                                promoted={item.promoted}
                                id={item.id}
                            />
                        ))}
                </div>
            </section>
            {category === "videojuegos" && (
                <div className="row my-5 home-type g-2">
                    <AllType />
                </div>
            )}
            <div className="divider"></div>
            <section className="my-5">
                <div className="horizontal-scrollable">
                    <div className="row flex-nowrap pt-1">
                        {category === 'videojuegos' ? (
                            store[category]?.filter((item) => !item.promoted).reverse()
                                .map((item) => (
                                    <VideogameCard
                                        key={item.id}
                                        img={item.img}
                                        name={item.name}
                                        brand={item.brand}
                                        price={item.price}
                                        promoted={item.promoted}
                                        id={item.id}
                                    />
                                ))
                        ) : (
                            store[category]
                                ?.filter((item) => !item.promoted).reverse()
                                .map((item) => (
                                    <ProductCard
                                        key={item.id}
                                        img={item.img}
                                        name={item.name}
                                        brand={item.brand}
                                        price={item.price}
                                        promoted={item.promoted}
                                        id={item.id}
                                    />
                                ))
                        )}
                    </div>
                </div>
            </section>

        </div>

    );
};