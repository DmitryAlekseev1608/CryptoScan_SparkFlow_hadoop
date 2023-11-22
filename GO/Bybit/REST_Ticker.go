package main

import (
  "fmt"
  "net/http"
  "io/ioutil"
  "regexp"
)

func main() {

  url := "https://api.bybit.com/v5/market/tickers?category=spot"
  method := "GET"

  client := &http.Client {
  }
  req, err := http.NewRequest(method, url, nil)

  if err != nil {
    fmt.Println(err)
    return
  }
  res, err := client.Do(req)
  if err != nil {
    fmt.Println(err)
    return
  }
  defer res.Body.Close()

  body, err := ioutil.ReadAll(res.Body)
  if err != nil {
    fmt.Println(err)
    return
  }
  fmt.Println(string(body)[0])

  re := regexp.MustCompile(`"symbol":\"(.*?)\",\"bid1Price`)
  fmt.Printf("%q\n", re.FindAllStringSubmatch(string(body), -1))
}