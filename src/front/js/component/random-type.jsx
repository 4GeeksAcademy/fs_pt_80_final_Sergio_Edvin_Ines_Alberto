import React, { useState, useEffect } from "react";
import "../../styles/types-home.css";
import { useNavigate } from "react-router-dom";

 export const GameType = () => {
    const navigate = useNavigate();
  

    const images = [
      { src: "https://res.cloudinary.com/dshjlidcs/image/upload/v1738526760/h0bz6rcrxcvsnpeb6lpr-min_c5to5i.png", title: "RPG", type: "RPG" },
      { src: "https://res.cloudinary.com/dshjlidcs/image/upload/v1738527220/web-img/fvvfnmm59tpsit5aenlt.png", title: "Acción", type: "accion" },
      { src: "https://res.cloudinary.com/dshjlidcs/image/upload/v1738526759/zgpzzo5l43zcheuwjlog-min_qfkuek.png", title: "Peleas", type: "pelea" },
      { src: "https://res.cloudinary.com/dshjlidcs/image/upload/v1738527219/web-img/lx7yilysmps9werakaxb.png", title: "Deportes", type: "deporte" },
      { src: "https://res.cloudinary.com/dshjlidcs/image/upload/v1738527220/web-img/fvvfnmm59tpsit5aenlt.png", title: "Aventura", type: "aventura" },
      { src: "https://res.cloudinary.com/dshjlidcs/image/upload/v1738526759/dmbrip698ff0wscqxhis-min_vkm11m.png", title: "Estrategia", type: "estrategia" },
      { src: "https://res.cloudinary.com/dshjlidcs/image/upload/v1738526761/pwk12gnwvcrakf6zjd4k-min_pg3mdf.png", title: "Horror", type: "horror" },
      { src: "https://res.cloudinary.com/dshjlidcs/image/upload/v1738526760/wa0vs74gpolv32oznuhh-min_r4bage.png", title: "Plataformas", type: "plataforma" },
      { src: "https://res.cloudinary.com/dshjlidcs/image/upload/v1738526760/ulnu3cjaxc3p3mzbvpqt-min_wgs5br.png", title: "Indie", type: "indie" },
    ];
  
    const [randomImages, setRandomImages] = useState([]);
  
    useEffect(() => {
      const shuffled = [...images].sort(() => 0.5 - Math.random()).slice(0, 3);
      setRandomImages(shuffled);
    }, []);
  
    
    const handleCategoryClick = (type) => {
      navigate(`/store/videogames/${type}`);
    };
  
    return (
      <div className="row my-5 home-type g-2">
        {randomImages.map((image, index) => (
          <div
            key={index}
            className="image-container  col-md-4"
            onClick={() => handleCategoryClick(image.type)}
            style={{ cursor: "pointer" }}
          >
            <img src={image.src} alt={image.title} />
            <div className="overlay">
              <span className="title">{image.title}</span>
            </div>
          </div>
        ))}
      </div>
    );
  };
  
 