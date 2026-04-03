package main

import (
	"fmt"
	"time"

	"github.com/gin-gonic/gin"
)

func Logger() gin.HandlerFunc {
	return func(c *gin.Context) {
		start := time.Now()
		c.Next()
		fmt.Println("LOG:", c.Request.Method, c.Request.URL.Path, time.Since(start))
	}
}