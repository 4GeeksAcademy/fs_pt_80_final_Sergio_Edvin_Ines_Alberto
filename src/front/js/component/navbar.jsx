import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import "../../styles/navbar.css";
import { useNavigate } from 'react-router-dom';
import { Context } from "../store/appContext";

import { CartItem } from "./shopping-cart-item.jsx"

export const Navbar = () => {
  const { store, actions } = useContext(Context)
  const [isTransparent, setIsTransparent] = useState(false);
  let lastScrollTop = 0;
  const [isCartOpen, setIsCartOpen] = useState(false);

  const handleScroll = () => {
    const currentScroll = window.scrollY;

    if (currentScroll > lastScrollTop) {
      setIsTransparent(true);
    } else {
      setIsTransparent(false);
    }

    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
  };

  useEffect(() => {
    window.addEventListener("scroll", handleScroll);
    actions.userShoppingCart()

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  useEffect(() => {
    if (store.shoppingCart.length > 0 || store.localShoppingCart.length > 0) {
      const offcanvasElement = document.getElementById("offcanvasShopping");
      if (offcanvasElement) {
        let offcanvasInstance = bootstrap.Offcanvas.getInstance(offcanvasElement);

        if (!offcanvasInstance) {
          offcanvasInstance = new bootstrap.Offcanvas(offcanvasElement);
        }

        if (!offcanvasElement.classList.contains("show")) {
          offcanvasInstance.show();
        }
      }
    }
  }, [store.shoppingCart, store.localShoppingCart]);

  const navigate = useNavigate();

  const handleLink = (type) => {
    if (type === "all") {
      navigate("/store");
    } else {
      navigate(`/store/${type}`);
    }
  };

  console.log("Usuario:", store.user ? store.user.userName : "Usuario no definido");
  console.log(store);
  console.log("ShoppingCart------->", store.shoppingCart)
  return (
    <>
      {/* Offcanvas del menú */}
      <div
        className={`offcanvas offcanvas-end ${isTransparent ? "transparent" : ""}`}
        tabIndex="-1"
        id="offcanvasNavbar"
        aria-labelledby="offcanvasNavbarLabel"
      >
        <div className="offcanvas-body my-offcanvas">
          <ul className="navbar-nav align-items-start flex-column">
            <li className="nav-item">
              <Link to="/contacto" className="nav-link my-offcanvas-text float" aria-current="page">
                CONTACTO
              </Link>
            </li>
            <li className="nav-item">
              <Link to="/perfil" className="nav-link my-offcanvas-text float">
                PERFIL
              </Link>
            </li>
            <li className="nav-item dropdown">
              <a
                className="nav-link dropdown-toggle my-offcanvas-text float"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                STORE
              </a>
              <ul className="dropdown-menu my-dropdown">
                <li>
                  <button
                    className="dropdown-item"
                    onClick={() => handleLink("all")}
                  >
                    Ver todo
                  </button>
                </li>
                <li>
                  <button
                    className="dropdown-item"
                    onClick={() => handleLink("consolas")}
                  >
                    Consolas
                  </button>
                </li>
                <li>
                  <button
                    className="dropdown-item"
                    onClick={() => handleLink("videojuegos")}
                  >
                    Videojuegos
                  </button>
                </li>
                <li>
                  <button
                    className="dropdown-item"
                    onClick={() => handleLink("accesorios")}
                  >
                    Accesorios
                  </button>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>

      {/* Offcanvas de la bolsa de compras */}
      <div
        className="offcanvas offcanvas-end offcanvas-shopping"
        tabIndex="-1"
        id="offcanvasShopping"
        aria-labelledby="offcanvasShoppingLabel"
      >

        <button type="button" className="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>

        <div className="offcanvas-body">
          {store.user ? (
            store.shoppingCart?.map((item) => (
              <CartItem
                key={item.id}
                img={item.img}
                name={item.name}
                seller_id={item.seller_id}
                price={item.price}
                id={item.id}
              />
            ))
          ) : (
            store.localShoppingCart?.map((item) => (
              <CartItem
                key={item.product_id}
                img={item.img}
                name={item.name}
                seller_id={item.seller_id}
                price={item.price}
                id={item.product_id}
              />
            ))
          )}

          <div className="divider"></div>
          <div className="text-center">
            <div className="total text-center">
              {store.user ?
                (store.shoppingCart?.reduce((total, item) => total + item.price, 0).toFixed(2) + "€") :
                (store.localShoppingCart?.reduce((total, item) => total + item.price, 0).toFixed(2) + "€")}
            </div>

            <Link to="/checkout" className="shopping-bar-button mt-5">Hacer pedido</Link>
            <div className="divider"></div></div>
        </div>
      </div>
      {/* Navbar principal */}
      <nav
        className={`navbar navbar-expand-lg my-navbar py-3 px-lg-3 px-0 sticky-top ${isTransparent ? "transparent" : ""
          }`}
      >
        <div className="container-fluid">
          <div className="col-2 text-center">
            <Link to="/">
              <img
                src="https://res.cloudinary.com/dr0wlij0c/image/upload/c_thumb,w_200,g_face/v1736453861/web-illustrations/logo.png"
                className="img-fluid"
                alt="Logo"
              />
            </Link>
          </div>
          <div className="d-flex">
            {/* Botón del menú */}
            <button
              className="my-navbar-toggler navbar-toggler"
              type="button"
              data-bs-toggle="offcanvas"
              data-bs-target="#offcanvasNavbar"
              aria-controls="offcanvasNavbar"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="fa-solid fa-bars menu-icon float"></span>
            </button>
            {/* Ícono de la bolsa de compras, se oculta en pantallas grandes */}
            <div>
              <span
                className={"fa-solid fa-bag-shopping small-device float"}
                alt="Shopping bag"
                data-bs-toggle="offcanvas"
                data-bs-target="#offcanvasShopping"
                aria-controls="offcanvasShopping"
              ></span>
            </div>
          </div>
          <div className="collapse navbar-collapse me-4" id="navbarSupportedContent">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0 mt-5 d-flex justify-content-between align-items-start">
              <li className="nav-item dropdown">
                <a
                  className="nav-link dropdown-toggle float my-dropdown"
                  href="#"
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  STORE
                </a>
                <ul className="dropdown-menu  my-dropdown">
                  <li>
                    <button
                      className="dropdown-item"
                      onClick={() => handleLink("all")}
                    >
                      Ver todo
                    </button>
                  </li>
                  <li>
                    <button
                      className="dropdown-item"
                      onClick={() => handleLink("consolas")}
                    >
                      Consolas
                    </button>
                  </li>
                  <li>
                    <button
                      className="dropdown-item"
                      onClick={() => handleLink("videojuegos")}
                    >
                      Videojuegos
                    </button>
                  </li>
                  <li>
                    <button
                      className="dropdown-item"
                      onClick={() => handleLink("accesorios")}
                    >
                      Accesorios
                    </button>
                  </li>
                </ul>
              </li>

              <div className="d-flex align-items-center">
                <li className="nav-item">
                  <Link to="/contacto" className="nav-link float" aria-current="page">
                    CONTACTO
                  </Link>
                </li>
                <li className="nav-item ms-3 float">
                  <Link to="/perfil" className="my-navbar-button px-3">
                    PERFIL
                  </Link>
                </li>
                <li className="nav-item nav-link float" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">
                  {/* Ícono de la bolsa de compras pantallas grandes, tambien abre el offcanvas */}
                  <span className={"fa-solid fa-bag-shopping nav-shopping-bag float"}
                    alt="Shopping bag"
                    data-bs-toggle="offcanvas"
                    data-bs-target="#offcanvasShopping"
                    aria-controls="offcanvasShopping"
                  ></span>
                </li>
              </div>

            </ul>
          </div>
        </div>
      </nav>
    </>
  );
};