package main

import (
	_ "go-service/docs"
	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

// @title Go Chat API
// @version 1.0
// @description WebSocket чат и REST API на Gin
// @host localhost:8080
// @BasePath /

func main() {
	r := gin.Default()
	r.Use(Logger())

	// @Summary Пинг
	// @Description Проверка работоспособности
	// @Success 200 {object} map[string]string
	// @Router /ping [get]
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{"message": "pong"})
	})

	// @Summary WebSocket чат
	// @Description Подключение к чату через WebSocket
	// @Success 101
	// @Router /ws [get]
	r.GET("/ws", HandleWebSocket)

	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	// Подключаем API gateway (будет ниже)
	setupGateway(r)

	go broadcaster()
	r.Run(":8080")
}