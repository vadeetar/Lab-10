package main

import (
	"net/http"
	"net/http/httputil"
	"net/url"
	"strings"

	"github.com/gin-gonic/gin"
)

func setupGateway(r *gin.Engine) {
	pythonURL, _ := url.Parse("http://localhost:8000")
	proxy := httputil.NewSingleHostReverseProxy(pythonURL)

	r.Any("/api/*proxyPath", func(c *gin.Context) {
		c.Request.URL.Path = strings.TrimPrefix(c.Request.URL.Path, "/api")
		proxy.ServeHTTP(c.Writer, c.Request)
	})

	r.GET("/gateway/status", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status": "ok",
			"services": gin.H{
				"go": "http://localhost:8080",
				"py": "http://localhost:8000",
			},
		})
	})
}