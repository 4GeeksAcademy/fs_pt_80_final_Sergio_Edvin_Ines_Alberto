import { React } from "react";

const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      isLogged: localStorage.getItem("Token") ? true : false,
      Token: localStorage.getItem("Token") || null,
      user: JSON.parse(localStorage.getItem("user")) || "",
      consolas: [],
      videojuegos: [],
      accesorios: [],
      subscriptions: [],
      selectedSubscriptions: [],
      selectedProduct: null,
      promoted: [],
      shoppingCart: [],
      localFavorites: [],
      localShoppingCart: [],
      users: [],
      orderSuccess: []
    },
    actions: {
      modStore: (key, value) => {
        setStore({ [key]: value })
      },

      //----------------------------------------------------LOGIN Y REGISTRO--------------------------------------------

      login: async (formData1) => {
        const actions = getActions();
        const store = getStore()
        try {
            const url = `${process.env.BACKEND_URL}/api/login`;
    
            // Recuperar los datos locales antes de loguear
            let localFavorites = JSON.parse(localStorage.getItem("localFavorites")) || [];
            let localShoppingCart = JSON.parse(localStorage.getItem("localShoppingCart")) || [];
    
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData1),
            });
    
            const data = await response.json();
    
            if (response.ok) {
                console.log("Login exitoso, usuario:", data.user);
   
                localStorage.setItem("Token", data.token);
                localStorage.setItem("user", JSON.stringify(data.user));
                setStore({ isLogged: true, Token: data.token, user: data.user });
    
                const userId = data.user.id;
    
                localFavorites = store.localFavorites.map(fav => ({
                    product_id: fav.product_id,
                    user_id: userId
                }));
    
                localShoppingCart = store.localShoppingCart.map(item => ({
                    product_id: item.product_id,
                    user_id: userId
                }));
    
                console.log("Enviando datos al backend:", { userId, localFavorites, localShoppingCart });
    
                // Enviar los datos locales al backend
                const mergeResponse = await fetch(`${process.env.BACKEND_URL}/api/merge-data`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${data.token}`
                    },
                    body: JSON.stringify({ userId, localFavorites, localShoppingCart })
                });
    
                const mergeData = await mergeResponse.json();
                console.log("Respuesta de la fusión de datos:", mergeData);
    
                if (mergeResponse.ok) {
                    console.log("Datos locales fusionados con éxito.")                    
                    setStore({ localFavorites: [], localShoppingCart: [] });  
                  
                    await actions.userShoppingCart();

                   
                } else {
                    console.error("Error al fusionar datos:", mergeData.msg);
                }
    
            } else {
                console.error("Error en el login:", data.msg);
            }
        } catch (error) {
            console.error("Error al conectar con el servidor:", error);
        }
    },
    
    

    register: async (formData) => {
      try {
          console.log("Datos del formulario para registro:", formData);
  
          //Recuperar los datos locales antes de registrarse
          let localFavorites = JSON.parse(localStorage.getItem("localFavorites")) || [];
          let localShoppingCart = JSON.parse(localStorage.getItem("localShoppingCart")) || [];
  
          console.log("Favoritos antes del registro:", localFavorites);
          console.log("Carrito antes del registro:", localShoppingCart);
  
          //Enviar los datos del usuario para registrarse
          const response = await fetch(`${process.env.BACKEND_URL}/api/register`, {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
              },
              body: JSON.stringify(formData),
          });
  
          const data = await response.json();
  
          if (response.ok) {
              console.log("Registro exitoso, usuario:", data.user);
              console.log("Token recibido:", data.token);
  
              localStorage.setItem("Token", data.token);
              localStorage.setItem("user", JSON.stringify(data.user));
              setStore({ isLogged: true, Token: data.token, user: data.user });
  
              const userId = data.user.id;
  
              // 🔹 Asociar favoritos y carrito al nuevo usuario
              const formattedFavorites = localFavorites.map(fav => ({
                  product_id: fav.product_id,
                  user_id: userId
              }));
  
              const formattedShoppingCart = localShoppingCart.map(item => ({
                  product_id: item.product_id,
                  user_id: userId
              }));
  
              console.log("Enviando datos al backend tras registro:", { userId, formattedFavorites, formattedShoppingCart });
  
              //Enviar los datos al backend para fusionarlos con la nueva cuenta
              const mergeResponse = await fetch(`${process.env.BACKEND_URL}/api/merge-data`, {
                  method: "POST",
                  headers: {
                      "Content-Type": "application/json",
                      Authorization: `Bearer ${data.token}`
                  },
                  body: JSON.stringify({ userId, localFavorites: formattedFavorites, localShoppingCart: formattedShoppingCart })
              });
  
              const mergeData = await mergeResponse.json();
              console.log("Respuesta de la fusión de datos tras registro:", mergeData);
  
              if (mergeResponse.ok) {
                  console.log("Datos locales fusionados con éxito tras registro.");
  
                  //Vaciar favoritos y carrito locales
                  localStorage.removeItem("localFavorites");
                  localStorage.removeItem("localShoppingCart");
                  setStore({ localFavorites: [], localShoppingCart: [] });
  
                  //Recargar el carrito desde el backend
                  await getActions().userShoppingCart();
                  await getActions().getFavorites();
              } else {
                  console.error("Error al fusionar datos tras registro:", mergeData.msg);
              }
          } else {
              console.error("Error en el registro:", data.msg || "Error desconocido");
          }
      } catch (error) {
          console.error("Error en el registro:", error);
      }
  },
  
  
    
      isLogged: async () => {
        try {
          const store = getStore();

          if (store.Token) {
            setStore({
              isLogged: true,
              user: JSON.parse(localStorage.getItem("user")),
            });
            await getActions().userShoppingCart();
          }
        }
        catch (error) {
          console.error("Error loading data:", error);
        }
      },

      updateUserProfile: async (userId, updatedData) => {
        const store = getStore();
        try {
            const token = store.Token;
            if (!token) {
                console.error("No se encontró un token válido");
                return null;
            }
    
            // Verifica que updatedData no esté vacío
            console.log("Datos que se van a actualizar:", updatedData);
    
            const response = await fetch(`${process.env.BACKEND_URL}/api/user/${userId}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify(updatedData)
            });
    
            if (!response.ok) {
                const errorDetails = await response.text(); // Obtener detalles del error del servidor
                console.error("Error al actualizar perfil, código:", response.status, "Detalles:", errorDetails);
                throw new Error("Error al actualizar perfil");
            }
    
            const data = await response.json();
            console.log("Perfil actualizado:", data);
            return data;
        } catch (error) {
            console.error("Error en updateUserProfile:", error);
            return null;
        }
    },
      //------------------------------------------------------LOAD INFO--------------------------------------------------

      loadInfo: async () => {
        try {
          const url = `${process.env.BACKEND_URL}/api/products`;
          const response = await fetch(url);
          const data = await response.json();

          const consolas = data.filter((item) => item.category === "consolas");
          const videojuegos = data.filter(
            (item) => item.category === "videojuegos"
          );
          const accesorios = data.filter(
            (item) => item.category === "accesorios"
          );
          const promoted = data.filter(
            (item) => item.promoted === true
          );

          const shuffleArray = (array) => array.sort(() => Math.random() - 0.5);

          setStore({
            consolas: shuffleArray(consolas),
            videojuegos: shuffleArray(videojuegos),
            accesorios: shuffleArray(accesorios),
            promoted: shuffleArray(promoted)
          });
        } catch (error) {
          console.error("Error loading data:", error);
        }
      },
      getAllReviews: async () => {
        const store = getStore();
        const actions = getActions();

        try {
          const response = await fetch(`${process.env.BACKEND_URL}/api/reviews`, {
            method: "GET",
          });

          if (response.ok) {
            const data = await response.json();
            const shuffleArray = (array) => array.sort(() => Math.random() - 0.5);
            setStore({ reviews: shuffleArray(data) });
          } else {
            console.error("Error al cargar las reseñas:", error);
          }
        } catch (error) {
          console.error("Error al cargar las reseñas:", error);
        }
      },

      getAllUsers: async () => {
        try {
          const store = getStore();
          const response = await fetch(`${process.env.BACKEND_URL}/api/users`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            }
          });

          const data = await response.json();

          if (response.ok) {
            setStore({ users: data });
          } else {
            console.error("Error al cargar los usuarios:", data);
          }
        } catch (error) {
          console.error("Error en la solicitud de usuarios:", error);
        }
      },

      //---------------------------------------------------GET SINGLE PRODUCT--------------------------------------------

      getProductById: async (id) => {
        try {
          const response = await fetch(`${process.env.BACKEND_URL}/api/product/${id}`);
          if (response.ok) {
            const data = await response.json();
            return data[0];
          } else {
            console.error("Error al obtener el producto:", response.statusText);
            return null;
          }
        } catch (error) {
          console.error("Error al conectar con el servidor:", error);
          return null;
        }
      },

      //------------------------------------------------------SELL PRODUCT-----------------------------------------------

      sellProduct: async (formData, navigate) => {
        const store = getStore();

        const payload = { ...formData, state: formData.state === "True", promoted: formData.promoted === "True" };
        console.log("Enviando datos a /api/product:", payload);

        try {
          const response = await fetch(`${process.env.BACKEND_URL}/api/product`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${store.Token}`,
            },
            body: JSON.stringify(payload),
          });

          const data = await response.json();

          if (response.ok) {
            setShowSuccess(true);
            navigate("/");
          } else {
            alert(data.msg || "Error al publicar el producto ⚠️ ");
          }
        } catch (error) {
          console.error("Error al publicar producto:", error);
          alert("Error al conectar con el servidor");
        }
      },

      //---------------------------------------------------------FAVS---------------------------------------------------

      toggleFav: async (newFav) => {
        const store = getStore();
        if (!store.Token) {
          return;
        }
        console.log("Datos enviados a favoritos:", newFav);

        try {
          const response = await fetch(`${process.env.BACKEND_URL}/api/favorites`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: store.Token ? `Bearer ${store.Token}` : "",
            },
            body: JSON.stringify(newFav),
          });

          const data = await response.json();

          if (response.ok) {
            console.log("Respuesta del servidor:", data);
            const updatedFavorites = data.updatedFavorites || [];
            setStore({ 
              user: { ...store.user, favorites: updatedFavorites },
              localFavorites: updatedFavorites.map(id => ({ product_id: id })) 
          });
          } else {
            console.error("Error del servidor:", data);
          }
        } catch (error) {
          console.error("Error de red:", error);
        }
      },

      removeFav: async (productId) => {
        const store = getStore();
        if (!store.Token) {
          return;
        }
      
        try {
          const response = await fetch(`${process.env.BACKEND_URL}/api/favorite/${productId}`, {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              Authorization: store.Token ? `Bearer ${store.Token}` : "",
            },
          });
      
          const data = await response.json();
      
          if (response.ok) {
            console.log("Respuesta del servidor:", data);
            const updatedFavorites = data.updatedFavorites || [];
            
            setStore({ 
              user: { ...store.user, favorites: updatedFavorites },
              localFavorites: updatedFavorites.map(id => ({ product_id: id }))
            });
          } else {
            console.error("Error del servidor:", data);
          }
        } catch (error) {
          console.error("Error de red:", error);
        }
      },

      toggleLocalFav: (newFav) => {
        const store = getStore();
    
        if (store.isLogged) {
            getActions().toggleFav(newFav);  
            return;
        }
    
        let updatedFavorites = [...store.localFavorites];
    
        // Verificar si el producto ya está en favoritos
        const isFavorite = updatedFavorites.some(el => el.product_id === newFav.product_id);
    
        if (isFavorite) {
            updatedFavorites = updatedFavorites.filter(el => el.product_id !== newFav.product_id);
        } else {
            updatedFavorites.push({ product_id: newFav.product_id });
        }
    
        setStore({ localFavorites: updatedFavorites });
        localStorage.setItem("localFavorites", JSON.stringify(updatedFavorites)); // Guardar en localStorage
    
        console.log("Favoritos locales guardados en localStorage:", JSON.parse(localStorage.getItem("localFavorites")));
    },

      //--------------------------------------------------------SHOPPING CART--------------------------------------------
      userShoppingCart: async () => {
        const store = getStore();
        const url = `${process.env.BACKEND_URL}/api/shopping-cart`;
        try {
          const response = await fetch(url, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${store.Token}`,
            },
          });

          if (response.ok) {
            const data = await response.json();
            setStore({ shoppingCart: data.shopping_cart_products });
          } else {
            console.error("Error al obtener el carrito de compras:", response.status);
          }
        } catch (error) {
          console.error("Error al conectar con el servidor:", error);
        }
      },

      toggleCart: async (newShoppingItem) => {

        const store = getStore();
        const actions = getActions();
        console.log("Datos enviados al carrito:", newShoppingItem);
        try {
          const response = await fetch(`${process.env.BACKEND_URL}/api/shopping_cart`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${store.Token}`,
            },
            body: JSON.stringify(newShoppingItem),
          });

          const data = await response.json();
          if (response.ok) {
            console.log("Respuesta del servidor:", data);
            const updatedUserShopping = data.updatedCart || [];
            const user = { ...store.user, shoppingCart: updatedUserShopping }
            setStore({ user });
            await actions.userShoppingCart()


          } else {
          }
        } catch (error) {
          console.error(error);
        }
      },

      toggleLocalCart: (newShoppingItem) => {
        const store = getStore();
    
        let updatedCart = [...store.localShoppingCart];
    
        const isInCart = updatedCart.some(el => el.product_id === newShoppingItem.product_id);
    
        if (isInCart) {
            updatedCart = updatedCart.filter(el => el.product_id !== newShoppingItem.product_id);
        } else {
            updatedCart.push({
                product_id: newShoppingItem.product_id,
                name: newShoppingItem.name,
                img: newShoppingItem.img,
                price: newShoppingItem.price
            });
        }
    
        setStore({ localShoppingCart: updatedCart });
        localStorage.setItem("localShoppingCart", JSON.stringify(updatedCart)); //Guardar en localStorage
    
        console.log("Carrito local guardado en localStorage:", JSON.parse(localStorage.getItem("localShoppingCart")));
    },

      //------------------------------------------------------UPLOAD_PHOTO-----------------------------------------------

      uploadImageToBackend: async (selectedFile) => {
        if (!selectedFile) {
          alert("Por favor, selecciona un archivo.");
          return null;
        }

        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
          const response = await fetch(`${process.env.BACKEND_URL}/api/upload`, {
            method: "POST",
            body: formData,
          });

          const data = await response.json();
          if (response.ok && data.secure_url) {
            return data.secure_url;
          } else {
            alert(data.error || "Error al subir la imagen.");
            return null;
          }
        } catch (error) {
          console.error("Error al subir la imagen:", error);
          alert("Error de conexión al subir la imagen.");
          return null;
        }
      },


      loadSubscriptions: async () => {
        try {
          const store = getStore();
          const response = await fetch(`${process.env.BACKEND_URL}/api/subscriptions`)
          const data = await response.json();

          if (response.ok) {
            setStore({ subscriptions: data });
          } else {
            console.error("Error loading suscriptions")
          }
        } catch (error) {
          console.error("Error fetching suscriptions", error)
        }
      },

      toggleSubscription: async (subscripionId) => {
        const store = getStore();
        let selectedSubscriptions = [...store.selectedSubscriptions]

        if (selectedSubscriptions.includes(subscripionId)) {
          selectedSubscriptions = selectedSubscriptions.filter(
            (id) => id !== subscripionId
          );
        } else {
          selectedSubscriptions.push(subscripionId);
        }
        setStore({ selectedSubscriptions });
      },

      setShowLoginModal: (value) => {
        const store = getStore();
        setStore({
          ...store,
          showLoginModal: value
        });
      },

      getFavorites: async () => {
        const store = getStore();
        const actions = getActions();

        try {
          const response = await fetch(`${process.env.BACKEND_URL}/api/favorites`, {
            method: "GET",
            headers: {
              "Authorization": `Bearer ${store.Token}`,
              "Content-Type": "application/json",
            },
          });

          if (response.ok) {
            const data = await response.json();
            // const favoriteIds = data.favorites.map((fav) => fav.product_id);

            // // Llamar al action para obtener detalles de cada producto
            // const favoriteProducts = await Promise.all(
            //     favoriteIds.map(async (productId) => {
            //         return await actions.getProductDetails(productId);
            //     })
            // );

            setStore({ favorites: data.favorite_products }); // Guardar los detalles de los productos favoritos
          } else {
            console.error("Error al obtener favoritos:", response.statusText);
          }
        } catch (error) {
          console.error("Error al conectar con el servidor:", error);
        }
      },

      getProductDetails: async (productId) => {
        const store = getStore();

        try {
          const response = await fetch(`${process.env.BACKEND_URL}/api/product/${productId}`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          });

          if (response.ok) {
            const data = await response.json();
            return data[0]; // El endpoint devuelve un array, seleccionamos el primer elemento
          } else {
            console.error(`Error al obtener el producto ${productId}:`, response.statusText);
          }
        } catch (error) {
          console.error(`Error al conectar con el servidor para el producto ${productId}:`, error);
        }
      },


      getUserProfile: async (userId) => {
        const store = getStore();

        try {
          const response = await fetch(`${process.env.BACKEND_URL}/api/users/${userId}`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          });

          if (response.ok) {
            const userData = await response.json();
            if (userId === store.user.id) {
              setStore({ user: userData });
              localStorage.setItem("user", JSON.stringify(userData)); // Actualiza el localStorage
            }
            return userData; // Devuelve los datos del usuario
          } else {
            console.error(`Error al obtener el perfil del usuario ${userId}:`, response.statusText);
          }
        } catch (error) {
          console.error(`Error al conectar con el servidor para el usuario ${userId}:`, error);
        }
      },

      followUser: async (userId) => {
        try {
          const store = getStore();

          const response = await fetch(`${process.env.BACKEND_URL}/api/users/follow`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${store.Token}` // Agregamos el token JWT
            },
            body: JSON.stringify({
              followed_id: userId, // Solo enviamos `followed_id`, ya que el backend obtiene `follower_id` del token JWT
            }),
          });

          if (response.ok) {
            console.log(`Usuario ${userId} seguido correctamente.`);
          } else {
            const errorData = await response.json();
            console.error("Error al seguir al usuario:", errorData);
          }
        } catch (error) {
          console.error("Error de red:", error);
        }
      },

      unfollowUser: async (userId) => {
        try {
          const store = getStore();
          const response = await fetch(`${process.env.BACKEND_URL}/api/users/unfollow/${userId}`, {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${store.Token}` // Agregamos el token JWT
            },
          });

          if (response.ok) {
            console.log(`Usuario ${userId} dejado de seguir correctamente.`);
          } else {
            const errorData = await response.json();
            console.error("Error al dejar de seguir al usuario:", errorData);
          }
        } catch (error) {
          console.error("Error de red:", error);
        }
      },

      logout: () => {
        localStorage.removeItem("Token");
        localStorage.removeItem("user");
        setStore({
          isLogged: false,
          Token: null,
          user: "",
        });
      },


      /* termina aqui */
    },
  };
};

export default getState;
