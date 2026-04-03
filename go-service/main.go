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

	r.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{"message": "pong"})
	})

	r.GET("/ws", HandleWebSocket)

	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	go broadcaster()

	r.Run(":8080")
}