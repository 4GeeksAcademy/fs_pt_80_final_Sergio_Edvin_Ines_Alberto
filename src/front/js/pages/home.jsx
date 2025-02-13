import React, { useContext, useEffect } from "react";
import { Context } from "../store/appContext";
import { Link } from "react-router-dom";
import "../../styles/home.css";

import { ProductCard } from "../component/product-small-card.jsx";
import { VideogameCard } from "../component/videogame-small-card.jsx";
import { Reviews } from "../component/reviews.jsx";
import { GameType } from "../component/random-type.jsx";
import { LoginModal } from "../component/login-modal.jsx";
//import { PremiumModal } from "../component/premium-modal.jsx";

export const Home = () => {
  const { store, actions } = useContext(Context);
   useEffect(() => {
                      window.scrollTo(0, 0); 
                      actions.setShowLoginModal(false); 
                  }, []);

  return (
    <div className="home-container">
       {store.showLoginModal && <LoginModal />}
        {/* <PremiumModal/> */}
      <section className="home-banners row my-5">
        <figure className=" col-12 col-lg-6">
          {" "}
          <Link to="/suscripcion">
            <img
              src="https://res.cloudinary.com/dshjlidcs/image/upload/v1738526760/imvwy8iwmkzk8mqskwzk-min_uhxbxt.png"
              alt=""
              className="img-fluid"
            />
          </Link>
        </figure>
        <figure className="col-12 col-lg-6">
          <Link to="/sell">
            <img
              src="https://res.cloudinary.com/dshjlidcs/image/upload/v1738526760/efzol3qocdcsps6rlczz-min_mlcoyz.png"
              alt=""
              className="img-fluid"
            />
          </Link>
        </figure>
      </section>
      <section className="my-5">
        <h3 className="t-seccion">Consolas</h3>
        <div className="horizontal-scrollable">
          <div className="row flex-nowrap pt-1">
            {store.consolas?.map((consola) => (
              <ProductCard
                key={consola.id}
                img={consola.img}
                name={consola.name}
                brand={consola.brand}
                price={consola.price}
                promoted={consola.promoted}
                id={consola.id}
              />
            ))}
          </div>
        </div>
      </section>
      <div className="divider"></div>
      <section className="my-5">
        <h3 className="t-seccion">Videojuegos</h3>
        <div className="horizontal-scrollable">
          <div className="row flex-nowrap pt-1">
            {store.videojuegos?.map((videojuego) => (
              <VideogameCard
                key={videojuego.id}
                img={videojuego.img}
                name={videojuego.name}
                brand={videojuego.brand}
                price={videojuego.price}
                promoted={videojuego.promoted}
                id={videojuego.id}
              />
            ))}
          </div>
        </div>
        <div className="row my-5 home-type g-2">
          <GameType />
        </div>
      </section>
      <div className="divider"></div>
      <section className="my-5">
        <h3 className="t-seccion">Accesorios</h3>
        <div className="horizontal-scrollable">
          <div className="row flex-nowrap pt-1">
            {store.accesorios?.map((accesorio) => (
              <ProductCard
                key={accesorio.id}
                img={accesorio.img}
                name={accesorio.name}
                brand={accesorio.brand}
                price={accesorio.price}
                promoted={accesorio.promoted}
                id={accesorio.id}
              />
            ))}
          </div>
        </div>
      </section>
      <div className="divider"></div>
      <section className="my-5 row">
        <h3 className="faq-home-h3">La mejor plataforma para comprar y vender.</h3>
        <p className="faq-home-p">Nuestros clientes nos avalan</p>
          <div className="row pt-1 d-flex justify-content-center justify-content-md-start">
          {store.reviews?.slice(0, 4).map((review) => (
              <Reviews
                key={review.id}
                user_id={review.user_id}
                rating={review.rating}
                comment={review.comment}
                product_id={review.product_id}
              />
            ))}
          </div>

      </section>
      <div className="divider"></div>
      <section className="row faq-home d-flex justify-content-md-start justify-content-center">
        <div className="col-10 col-lg-9">
          <h3 className="faq-home-h3">¿Tienes dudas?</h3>
          <p className="faq-home-p">Consulta nuestras <Link to="/contacto" className="faq-home-p-a">preguntas frecuentes</Link></p>
          <Link to="/suscripcion" className="faq-home-button">Go premium</Link>
          <p className="faq-home-p">Contacto directo y mucho más...</p>
        </div>
        <figure className=" col-8 col-lg-3 text-md-start text-center ms-lg-0">
          <img src="https://res.cloudinary.com/dshjlidcs/image/upload/v1738526760/r5r3z9kfuqd95yennokv-min_mcza4i.png" alt="FAQ" className="img-fluid" />
        </figure>
      </section>
      <div className="divider"></div>
    </div>
  );
};
