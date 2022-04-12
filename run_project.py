import uvicorn

if __name__ == '__main__':
    uvicorn.run("retailer.app.application:app", port=8080, reload=True)